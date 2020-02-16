import youtube_dl
import easygui
from pathlib import Path


def download_yt(video_url, destination_folder):
    if 'playlist' in video_url or 'list' in video_url:
        path = destination_folder + Path('/%(playlist)s/%(playlist_index)s _ %(title)s.%(ext)s')
        ydl = youtube_dl.YoutubeDL({'outtmpl': path})
    else:
        path = destination_folder + Path('/%(title)s.%(ext)s')
        ydl = youtube_dl.YoutubeDL({'outtmpl': path})

    with ydl:
        result = ydl.extract_info(
            video_url,
            download=True
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        for video in result['entries']:
            print(video['webpage_url'])
            print(video['title'])
    else:
        # Just a video
        video = result
        print(video['webpage_url'])
        print(video['title'])


if __name__ == "__main__":
    print("Donne moi l'adresse youtube")
    while True:
        video_url = input('>')
        if 'www.youtube.com/' in video_url:
            break
        else:
            print("Ceci n'est pas une adresse youtube, reessayer")
            continue
    destination_folder = easygui.diropenbox()
    print("Destination folder: ", destination_folder)
    download_yt(video_url, destination_folder)
