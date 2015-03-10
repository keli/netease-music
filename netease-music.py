#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os
import sys
import md5
import string
import random

# Set cookie
cookie_opener = urllib2.build_opener()
cookie_opener.addheaders.append(('Cookie', 'appver=2.0.2'))
cookie_opener.addheaders.append(('Referer', 'http://music.163.com'))
urllib2.install_opener(cookie_opener)

def encrypted_id(id):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2')
    byte2 = bytearray(id)
    byte1_len = len(byte1)
    for i in xrange(len(byte2)):
        byte2[i] = byte2[i]^byte1[i%byte1_len]
    m = md5.new()
    m.update(byte2)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

def get_playlist(playlist_id):
    url = 'http://music.163.com/api/playlist/detail?id=%s' % playlist_id
    resp = urllib2.urlopen(url)
    data = json.loads(resp.read())
    return data['result']

def save_track(track, folder, position):
    name = track['hMusic']['name']

    if position < 10:
        pos = "0%d" % position
    else:
        pos = "%d" % position

    #fname = pos + ' ' + name + track['hMusic']['extension']
    fname = name + '.' + track['hMusic']['extension']
    fname = string.replace(fname, '/', '_')
    fpath = os.path.normpath(os.path.join(folder, fname))

    if os.path.exists(fpath):
        return

    print "Downloading", fpath, "..."

    dfsId = str(track['hMusic']['dfsId'])
    url = 'http://m%d.music.126.net/%s/%s.%s' % (random.randrange(1, 3), encrypted_id(dfsId), dfsId, track['hMusic']['extension'])
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

