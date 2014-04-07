#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os
import sys
import string

# Set cookie
cookie_opener = urllib2.build_opener()
cookie_opener.addheaders.append(('Cookie', 'appver=1.7.1'))
urllib2.install_opener(cookie_opener)

def get_playlist(playlist_id):
    url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
    resp = urllib2.urlopen(url)
    data = json.loads(resp.read())
    return data['result']

def save_track(track, folder, position):
    name = track['name']

    if position < 10:
        pos = "0%d" % position
    else:
        pos = "%d" % position

    fname = pos + ' ' + name + '.mp3'
    fname = string.replace(fname, '/', '_')
    fpath = os.path.normpath(os.path.join(folder, fname))

    if os.path.exists(fpath):
        return

    print "Downloading", fpath, "..."

    resp = urllib2.urlopen(track['mp3Url'])
    data = resp.read()
    resp.close()

    with open(fpath, 'wb') as mp3:
      mp3.write(data)

def download_playlist(playlist_id, folder='.'):
    playlist = get_playlist(playlist_id)

    name = playlist['name']
    folder = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    for idx, track in enumerate(playlist['tracks']):
        save_track(track, folder, idx+1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s <playlist id>" % sys.argv[0] 
        sys.exit(1)
    download_playlist(sys.argv[1])

