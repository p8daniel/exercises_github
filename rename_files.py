import sys
import os

for i in range(len(sys.argv) - 1):
    path, filename = os.path.split(os.path.abspath(sys.argv[i + 1]))
    if not '.mp4' in filename:
        filename2 = filename + '.mp4'
        os.rename(os.path.join(path, filename), os.path.join(path, filename2))
        print('renamed', filename2)
