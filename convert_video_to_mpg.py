import os

import easygui
from ffmpy import FFmpeg


# https://www.youtube.com/watch?v=qjtmgCb8NcE

def convert_video(mp4_video_path):
    if mp4_video_path.endswith('.mp4'):
        mpg_video_path = mp4_video_path.replace('.mp4', '.mpg')
        print(mpg_video_path)
        ff = FFmpeg(executable='C:\\Program_Files\\ffmpeg\\bin', inputs={mp4_video_path: None},
                    outputs={mpg_video_path: None})
        # ff.cmd_str
        # Out[2]: 'ffmpeg -i /tmp/input.ts /tmp/output.mp4'
        ff.run()


if __name__ == "__main__":
    destination_folder = easygui.diropenbox()
    print("Destination folder: ", destination_folder)
    for file in os.listdir(destination_folder):
        if file.endswith('.mp4'):
            print("converting", file)
            convert_video(file)
