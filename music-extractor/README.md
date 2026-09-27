# music-extractor

Download audio from supported online videos, or extract it from an existing, unprotected local video file. Use only for media you are permitted to download and process. DRM-protected material is not supported.

## Setup (Windows / PowerShell)

From the `music-extractor` directory, with your Python virtual environment activated:

```powershell
python -m pip install -U -r requirements.txt
```

Install FFmpeg (including `ffprobe`) and make sure both commands are on PATH. To use YouTube, install Deno 2.3+ and make sure `deno --version` works. Current yt-dlp uses external JavaScript challenge scripts; `yt-dlp[default]` installs the matching `yt-dlp-ejs` Python component. See https://github.com/yt-dlp/yt-dlp/wiki/EJS.

To use the BBC iPlayer route, separately install `get_iplayer` and verify `get_iplayer --version`. This tool is not a Python package and availability depends on the programme, broadcaster restrictions and your location.

## Examples

The original two-position-argument invocation is retained, producing a 192 kbps MP3 by default:

```powershell
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" "My Audio"
```

Prefer audio-only M4A (AAC streams are preferred by the downloader):

```powershell
python main.py "https://www.youtube.com/watch?v=VIDEO_ID" "My Audio" --format m4a
```

Download a supported playlist into its own numbered folder:

```powershell
python main.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" "Rownd a Rownd - Series 1" --playlist --format m4a
```

Use browser cookies *only when needed* (Firefox, Chrome, Edge or Vivaldi):

```powershell
python main.py "VIDEO_URL" "My Audio" --browser vivaldi
```

Extract the first audio stream of a local media file (AAC -> M4A uses stream copy; otherwise re-encodes):

```powershell
python main.py ".\episode.mp4" "Rownd a Rownd - Episode 01" --format m4a
```

Try a supported BBC iPlayer episode, where permitted/available:

```powershell
python main.py "https://www.bbc.co.uk/iplayer/episode/EPISODE_PID/episode-name" "Episode 01" --format m4a
```

Request subtitle files when offered for online content:

```powershell
python main.py "VIDEO_URL" "Episode 01" --format m4a --subtitles
```

Custom output directory: `--output-dir "D:\Welsh Audio"`. Run `python main.py --help` for all options. Files go to `./out` by default and are excluded from Git by the existing project .gitignore.

## Notes

- `--playlist` is explicit; a single-video link does not silently expand into a playlist.
- The default is MP3 for yt-dlp URLs (backward compatibility), M4A for local and iPlayer sources.
- M4A is a container, and non-AAC sources may be re-encoded by FFmpeg.
- Support for S4C Clic URLs depends on the currently installed yt-dlp extractor and programme availability. The script passes such URLs through yt-dlp; it does not bypass access restrictions.
- iPlayer is handled through `get_iplayer --audio-only`. The script does not attempt to circumvent DRM.
- Requested subtitles may not be available for every episode or language.
