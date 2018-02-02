from pytube import YouTube
import requests
from bs4 import BeautifulSoup


def download_video(link, download_dir):
    yt = YouTube(link)
    videos = yt.streams.filter(file_extension='mp4').all()
    for v in videos:
        v.download(download_dir)


def download_playlist(playlist_url, download_dir):
    r = requests.get(playlist_url)
    soup = BeautifulSoup(r.content, 'lxml')
    video_links = set([e.get('href') for e in soup.find_all('a') if 'watch' in e.get('href')])
    for link in video_links:
        download_video(link, download_dir)


playlist_url = "https://www.youtube.com/playlist?list=PLEuGrYl8iBm4j83wiDenn9sQh4g1_gmqQ"
download_dir = 'Hardware_Tutorials'

download_playlist(playlist_url, download_dir)