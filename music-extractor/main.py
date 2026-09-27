"""Extract audio from supported online videos or an existing local media file.

Legacy usage remains: python main.py URL filename
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def safe_name(value):
    """Keep the filename prefix portable and inside the chosen output folder."""
    if (
        not value
        or value in {".", ".."}
        or value.endswith((" ", "."))
        or re.search(r'[<>:"/\\|?*\x00-\x1f]', value)
    ):
        raise ValueError("Name must be a simple filename prefix (no path or special characters).")
    return value


def require_executable(name):
    if not shutil.which(name):
        raise RuntimeError(
            f"{name} was not found on PATH. Install it and restart your terminal."
        )


def source_kind(source):
    if Path(source).is_file():
        return "local"
    parsed = urlparse(source)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Supply an existing local file or an http(s) programme URL.")
    host = parsed.hostname or ""
    if host in {"bbc.co.uk", "www.bbc.co.uk", "bbc.com", "www.bbc.com"} and parsed.path.startswith("/iplayer/"):
        return "iplayer"
    return "yt-dlp"


def extract_local(source, name, output_dir, audio_format):
    """Copy existing AAC audio to M4A; encode only when the codec requires it."""
    require_executable("ffmpeg")
    require_executable("ffprobe")
    destination = output_dir / f"{name}.{audio_format}"
    if destination.exists():
        raise FileExistsError(f"Output already exists: {destination}")

    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name", "-of",
            "default=noprint_wrappers=1:nokey=1", str(source),
        ],
        check=True, text=True, capture_output=True,
    )
    codec = probe.stdout.strip()
    if not codec:
        raise RuntimeError("No audio stream was found in the local file.")

    if audio_format == "m4a" and codec == "aac":
        audio_args = ["-c:a", "copy"]
    elif audio_format == "m4a":
        audio_args = ["-c:a", "aac", "-b:a", "192k"]
    else:
        audio_args = ["-c:a", "libmp3lame", "-b:a", "192k"]

    subprocess.run(
        [
            "ffmpeg", "-n", "-i", str(source), "-map", "0:a:0",
            "-vn", *audio_args, str(destination),
        ],
        check=True,
    )
    print(f"Audio saved: {destination}")


def download_iplayer(url, name, output_dir, audio_format, subtitles):
    """Use the independently installed get_iplayer, where programmes are available."""
    require_executable("get_iplayer")
    if audio_format != "m4a":
        raise ValueError(
            "get_iplayer produces M4A audio. Omit --format, or choose --format m4a. "
            "You can convert a downloaded file to MP3 using local-file mode."
        )
    match = re.match(r"^/iplayer/episode/([a-z0-9]+)(?:/|$)", urlparse(url).path)
    if not match:
        raise ValueError("Expected a BBC iPlayer episode URL containing its programme PID.")
    command = [
        "get_iplayer", f"--pid={match.group(1)}", "--audio-only",
        "--output", str(output_dir), "--file-prefix", name,
    ]
    if subtitles:
        command.append("--subtitles")
    subprocess.run(command, check=True)
    print(f"get_iplayer finished. Check {output_dir} for the M4A file.")


def download_ytdlp(url, name, output_dir, audio_format, browser, playlist, subtitles):
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError(
            'yt-dlp is not installed. Run: python -m pip install -U "yt-dlp[default]"'
        ) from exc
    require_executable("ffmpeg")

    if playlist:
        template = str(
            output_dir / name / "%(playlist_index)03d - %(title).100B [%(id)s].%(ext)s"
        )
    else:
        template = str(output_dir / f"{name}.%(ext)s")

    options = {
        "format": "bestaudio[ext=m4a]/bestaudio/best" if audio_format == "m4a" else "bestaudio/best",
        "outtmpl": template,
        "noplaylist": not playlist,
        "windowsfilenames": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                **({"preferredquality": "192"} if audio_format == "mp3" else {}),
            }
        ],
    }
    if browser != "none":
        options["cookiesfrombrowser"] = (browser,)
    if subtitles:
        options.update({
            "writesubtitles": True,
            "subtitleslangs": ["cy", "en"],
            "subtitlesformat": "srt/best",
        })

    with yt_dlp.YoutubeDL(options) as ydl:
        result = ydl.download([url])
    if result:
        raise RuntimeError(f"yt-dlp reported a download error (exit code {result}).")
    print(f"Audio saved under: {output_dir}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Download or extract an audio track for personal listening, where permitted."
    )
    parser.add_argument("source", help="Video URL, BBC iPlayer episode URL, or local media file")
    parser.add_argument("name", help="Output filename prefix (or playlist subfolder)")
    parser.add_argument(
        "--format", choices=("mp3", "m4a"), default=None,
        help="Audio format; defaults to MP3 for yt-dlp and M4A for iPlayer/local files",
    )
    parser.add_argument(
        "--browser", choices=("none", "firefox", "chrome", "edge", "vivaldi"),
        default="none", help="Use browser cookies when needed (default: none)",
    )
    parser.add_argument("--playlist", action="store_true", help="Download the entire playlist")
    parser.add_argument("--subtitles", action="store_true", help="Request Welsh/English subtitles, when offered")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("out"),
        help="Output directory (default: ./out)",
    )
    args = parser.parse_args(argv)

    try:
        name = safe_name(args.name)
        kind = source_kind(args.source)
        if args.playlist and kind != "yt-dlp":
            raise ValueError("--playlist is only supported for yt-dlp URLs.")
        if args.subtitles and kind == "local":
            raise ValueError("--subtitles is only supported for online programmes.")
        audio_format = args.format or ("mp3" if kind == "yt-dlp" else "m4a")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        if kind == "local":
            extract_local(Path(args.source), name, args.output_dir, audio_format)
        elif kind == "iplayer":
            download_iplayer(args.source, name, args.output_dir, audio_format, args.subtitles)
        else:
            download_ytdlp(
                args.source, name, args.output_dir, audio_format,
                args.browser, args.playlist, args.subtitles,
            )
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
