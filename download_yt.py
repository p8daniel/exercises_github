import os

import youtube_dl

# import easygui
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from webptools import dwebp
from PIL import Image

ONLY_AUDIO = True

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

ydl_opts_video = {
    # 'format': 'bestaudio/best',  # choice of quality
    # 'format': '140/134',  # choice of quality ; see formats above
    # 'extractaudio': True,  # only keep the audio
    # "ignoreerrors": True
}

ydl_opts_audio = {
    "writethumbnail": True,
    # 'format': 'bestaudio/best',  # choice of quality
    "format": "140/134",  # choice of quality ; see formats above
    # 'extractaudio': True,  # only keep the audio
    # 'audioformat': "mp3",  # convert to mp3
    # 'outtmpl': '%(id)s',  # name the file the ID of the video
    # 'noplaylist': True,  # only download single song, not playlist
    #
    "postprocessors": [
        {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192",}
    ],
    # 'postprocessors': [{
    #     'key': 'FFmpegVideoConvertor',
    #     'preferedformat': 'avi',
    # }],
    "ignoreerrors": True,
}


def download_yt(video_url, destination_folder, ydl_opts):
    if "playlist" in video_url or "list" in video_url:
        path = destination_folder + str(
            Path("/%(playlist)s/%(playlist_index)s _ %(title)s.%(ext)s")
        )
    else:
        path = destination_folder + str(Path("/%(title)s.%(ext)s"))

    ydl_opts["outtmpl"] = path

    ydl = youtube_dl.YoutubeDL(ydl_opts)

    with ydl:
        result = ydl.extract_info(video_url, download=True)

    if "entries" in result:
        result_titles = []
        # Can be a playlist or a list of videos
        for video in result["entries"]:
            print(video["webpage_url"])
            print(video["title"])
            result_titles.append(video["title"])
        return result_titles
    else:
        # Just a video
        video = result
        print(video["webpage_url"])
        print(video["title"])
        print(video["format"])
    return [video["title"]]


def add_cover_mp3(destination_folder, title):
    audio_path = Path(destination_folder + title + ".mp3")

    picture_path_webp_to_fix = Path(destination_folder + title + ".webp")

    if os.path.exists(picture_path_webp_to_fix):

        picture_path_jpg = Path(destination_folder + "cover" + ".jpg")
        picture_path_webp = Path(destination_folder + "cover" + ".webp")

        if os.path.exists(picture_path_webp):
            os.remove(picture_path_webp)
        if os.path.exists(picture_path_jpg):
            os.remove(picture_path_jpg)
        os.rename(picture_path_webp_to_fix, picture_path_webp)

        # dwebp(picture_path_webp, picture_path_jpg, "-o")
        im = Image.open(picture_path_webp).convert("RGB")
        im.save(picture_path_jpg)
        picture_path = picture_path_jpg
        os.remove(picture_path_webp)

    else:
        picture_path = destination_folder + title + ".jpg"

    if os.path.exists(picture_path):
        audio = MP3(audio_path, ID3=ID3)
        # adding ID3 tag if it is not present
        try:
            audio.add_tags()
        except:
            pass
        audio.tags.add(
            APIC(mime="image/jpeg", type=3, desc=u"Cover", data=open(picture_path, "rb").read(),)
        )
        # edit ID3 tags to open and read the picture from the path specified and assign it
        audio.save()  # save the current changes
        os.remove(picture_path)
    else:
        raise Exception("picture not found")


if __name__ == "__main__":
    print("Donne moi l'adresse youtube")
    while True:
        video_url = input(">")
        if "www.youtube.com/" in video_url:
            break
        else:
            print("Ceci n'est pas une adresse youtube, reessayer")
            continue

    # destination_folder = easygui.diropenbox()

    if ONLY_AUDIO:
        destination_folder = "/home/daniel.pelati/Music/"
        print("Destination folder: ", destination_folder)
        titles = download_yt(video_url, destination_folder, ydl_opts_audio)

        for title in titles:
            title = title.replace("|", "_").replace(":", " -")
            add_cover_mp3(destination_folder, title)
    else:
        destination_folder = "/home/daniel.pelati/Videos/"
        print("Destination folder: ", destination_folder)
        download_yt(video_url, destination_folder, ydl_opts_video)
