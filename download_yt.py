import youtube_dl
import easygui
from pathlib import Path


# https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
# https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme
# https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection

# format code extension resolution  note
# 140         m4a       audio only  DASH audio , audio@128k (worst)
# 160         mp4       144p        DASH video , video only
# 133         mp4       240p        DASH video , video only
# 134         mp4       360p        DASH video , video only
# 135         mp4       480p        DASH video , video only
# 136         mp4       720p        DASH video , video only
# 17          3gp       176x144
# 36          3gp       320x240
# 5           flv       400x240
# 43          webm      640x360
# 18          mp4       640x360
# 22          mp4       1280x720    (best)

def download_yt(video_url, destination_folder):
    if 'playlist' in video_url or 'list' in video_url:
        path = destination_folder + str(Path('/%(playlist)s/%(playlist_index)s _ %(title)s.%(ext)s'))
    else:
        path = destination_folder + str(Path('/%(title)s.%(ext)s'))

    ydl_opts = {
        'writethumbnail': True,
        # 'format': 'bestaudio/best',  # choice of quality
        'format': '140/134',  # choice of quality ; see formats above
        # 'extractaudio': True,  # only keep the audio
        # 'audioformat': "mp3",  # convert to mp3
        # 'outtmpl': '%(id)s',  # name the file the ID of the video
        # 'noplaylist': True,  # only download single song, not playlist
        #
        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        #     'preferredquality': '192',
        # }],

        # 'postprocessors': [{
        #     'key': 'FFmpegVideoConvertor',
        #     'preferedformat': 'avi',
        # }],

        'outtmpl': path,
        'ignoreerrors': True
    }

    ydl = youtube_dl.YoutubeDL(ydl_opts)

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
        print(video['format'])
        # print(info_dict.get('thumbnail'))


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
