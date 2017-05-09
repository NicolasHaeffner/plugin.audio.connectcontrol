import os
import io
import xbmcgui
from PIL import Image, ImageFilter
import urllib2 as urllib


def blurCover(coverurl, cachepath):
    savepath = os.path.join(cachepath, coverurl.rsplit('/', 1)[-1] + '.jpg')
    if os.path.isfile(savepath):
        return savepath
    else:
        cover = Image.open(io.BytesIO(urllib.urlopen(coverurl).read()))
        cover_blurred = cover.filter(ImageFilter.GaussianBlur(80))
        cover_blurred = cover_blurred.point(lambda p: p * 0.5)
        cover_blurred.save(savepath)
        return savepath


def secondsToString(secstr):
    minutes, seconds = divmod(int(secstr), 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)
    minstr = str(minutes) + ':' + seconds
    return minstr


def getArtists(track):
    artists = track['item']['artists'][0]['name']
    if len(track['item']['artists']) == 1:
        return artists
    else:
        iterartists = iter(track['item']['artists'])
        next(iterartists)
        for artist in iterartists:
            artists += ' & ' + artist['name']
        return artists


def chooseDevice(devices):
    names = []
    for i, val in enumerate(devices):
        names.append(val['name'])
    dialog = xbmcgui.Dialog()
    ret = dialog.select('Choose a Device', names)
    if ret == -1:
        return False
    else:
        return devices[ret]['id']
