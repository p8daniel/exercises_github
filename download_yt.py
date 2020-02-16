import youtube_dl


def download_yt():
    videos = []
    # ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
    # ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s%(ext)s'})
    ydl = youtube_dl.YoutubeDL({'outtmpl': '/media/daniel/SDXC200/Video/%(playlist)s/%(playlist_index)s _ %(title)s.%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            'https://www.youtube.com/playlist?list=PLnCADODAJAAVos2ROUdvYjhUaBEEk6dwP',
            download=True  # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        for video in result['entries']:
            print(video['webpage_url'])
            print(video['title'])
    else:
        # Just a video
        video = result

    # print(video)


if __name__ == "__main__":
    download_yt()
