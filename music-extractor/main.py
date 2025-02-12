import sys
import yt_dlp

#url = "https://www.youtube.com/watch?v=UDORqIhOPWM"
url = sys.argv[1]
outfname = sys.argv[2]

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'./out/{outfname}.%(ext)s',
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download complete!")

