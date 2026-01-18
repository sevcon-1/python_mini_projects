'''
    Simple script to download YT audio from a provided url
    Usage: main.py <YT url> <Target file prefix>
'''

import sys
import yt_dlp

#url = "https://www.youtube.com/watch?v=UDORqIhOPWM"
url = sys.argv[1]
outfname = sys.argv[2]

browser = 'firefox'

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'./out/{outfname}.%(ext)s',
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    'cookiesfrombrowser': (browser,),  # Use cookies from the specified browser
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download complete!")

