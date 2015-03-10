#!/usr/bin/env python
import os
import glob

dir = os.getcwd()

for (path, subdirs, files) in os.walk(dir):
    os.chdir(path)
    if glob.glob("*.mp3") != []:
        _m3u = open( os.path.split(path)[1] + ".m3u" , "w" )
        for song in glob.glob("*.mp3"):
            _m3u.write(song + "\n")
        _m3u.close()

os.chdir(dir)
