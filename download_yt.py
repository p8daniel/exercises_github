import youtube_dl
import easygui
from pathlib import Path



# https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
# https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme
# https://www.youtube.com/watch?v=qZ8zTmowSgo&list=PL6Iy9ukHIwgxkXlvBQyYzXHNQT73W7Dgf
# https://www.youtube.com/watch?v=uhSCf5KMANo&list=PL6Iy9ukHIwgz4tKdcNwFOeS4GmDhhlqXe

def download_yt(video_url, destination_folder):
    if 'playlist' in video_url or 'list' in video_url:
        path = destination_folder + str(Path('/%(playlist)s/%(playlist_index)s _ %(title)s.%(ext)s'))
        ydl = youtube_dl.YoutubeDL({'outtmpl': path, 'ignoreerrors': True})
    else:
        path = destination_folder + str(Path('/%(title)s.%(ext)s'))
        ydl = youtube_dl.YoutubeDL({'outtmpl': path, 'ignoreerrors': True})

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
