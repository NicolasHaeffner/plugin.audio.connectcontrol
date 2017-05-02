from __future__ import division
import os
import time
import xbmc
import xbmcaddon
import xbmcgui
import resources.lib.helpers as helpers
import resources.lib.spotipyControl as spotipyControl
import resources.lib.spotipy.util as util
from threading import Thread


# get addon info and set globals
addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')
addon_id = addon.getAddonInfo('id').decode("utf-8")
cachepath = xbmc.translatePath(u"special://profile/addon_data/%s/" % (addon_id,)).decode("utf-8")
username = addon.getSetting('username')
client_id = addon.getSetting('client_id')
client_secret = addon.getSetting('client_secret')

# Worker Thread that checks the server for changes
windowopen = True   # global used to tell the worker thread the status of the window


def updateWindow(name, gui):
    time.sleep(0.5)
    track_old = {'item': '', 'is_playing': False, 'shuffle_state': 'off'}
    while windowopen and (not xbmc.abortRequested):
        track = sp.get_player()
        if track['item'] != track_old['item'] or track['is_playing'] != track_old['is_playing'] or track['shuffle_state'] != track_old['shuffle_state'] or track['repeat_state'] != track_old['repeat_state']:
            # insert update functions here
            gui.onUpdate(track)
            track_old = track
        gui.setProgress(track['progress_ms'], track['item']['duration_ms'])
        time.sleep(1)


# Define the GUI
class Main(xbmcgui.WindowXML):

    def __init__(self, *args, **kwargs):
        pass

    def onInit(self):
        # define controls
        self.win = xbmcgui.Window(10001)
        self.background = self.getControl(1001)
        self.cover = self.getControl(1002)
        self.play = self.getControl(1101)
        self.pause = self.getControl(1102)
        self.progress = self.getControl(3001)
        self.shuffle = self.getControl(1008)
        # self.repeat = self.getControl(1007)
        self.inLib = self.getControl(1009)
        self.next = self.getControl(1005)
        self.previous = self.getControl(1006)
        self.repeat_all = self.getControl(1201)
        self.repeat_one = self.getControl(1202)
        self.repeat_off = self.getControl(1203)
        self.volume_button = self.getControl(1011)

    def onAction(self, action):
        if action.getId() == 79:
            self.togglePlayState()
        elif action.getId() == 92:
            self.close()

    def onClick(self, controlID):
        if controlID == 1101:
            sp.play()
        if controlID == 1102:
            sp.pause()
        if controlID == 1005:
            sp.next()
        if controlID == 1006:
            sp.previous()
        if controlID == 1008:
            if self.shuffle.isSelected():
                sp.shuffle(True)
            else:
                sp.shuffle(False)
        if controlID == 1201:
            sp.repeat('track')
        if controlID == 1202:
            sp.repeat('off')
        if controlID == 1203:
            sp.repeat('context')
        if controlID == 1009:
            track = sp.get_player()
            if sp.current_user_saved_tracks_contains([track['item']['uri']])[0] is False:
                sp.current_user_saved_tracks_add([track['item']['uri']])
            elif sp.current_user_saved_tracks_contains([track['item']['uri']])[0] is True:
                sp.current_user_saved_tracks_delete([track['item']['uri']])
        if controlID == 1011:
            sp.put_player(helpers.chooseDevice(sp.get_devices()['devices']))

    def onUpdate(self, track):
        coverurl = track['item']['album']['images'][0]['url']
        self.cover.setImage(coverurl, False)
        self.background.setImage(helpers.blurCover(coverurl, cachepath), False)
        self.win.setProperty('title', track['item']['name'])
        self.win.setProperty('artist', helpers.getArtists(track))
        self.win.setProperty('album', track['item']['album']['name'])
        self.choseRepeat(track['repeat_state'])
        self.togglePlayPause(track['is_playing'])
        self.shuffle.setSelected(track['shuffle_state'])
        self.win.setProperty('device', track['device']['name'])

    def setProgress(self, progress_ms, duration_ms):
        progress = (100 * progress_ms) / duration_ms
        self.progress.setPercent(100 - progress)
        self.win.setProperty('progressTime', helpers.secondsToString(progress_ms // 1000))
        self.win.setProperty('remainingTime', '- ' + helpers.secondsToString((duration_ms - progress_ms) // 1000))

    def togglePlayPause(self, is_playing):
        self.pause.setVisible(is_playing)
        if is_playing:
            self.next.controlLeft(self.pause)
            self.previous.controlRight(self.pause)
        else:
            self.setFocus(self.play)
            self.next.controlLeft(self.play)
            self.previous.controlRight(self.play)

    def choseRepeat(self, repeat_state):
        if repeat_state == 'context':
            self.repeat_all.setVisible(True)
            self.repeat_one.setVisible(False)
            self.repeat_off.setVisible(False)
            self.volume_button.controlLeft(self.repeat_all)
            self.next.controlRight(self.repeat_all)

        if repeat_state == 'track':
            self.repeat_all.setVisible(False)
            self.repeat_one.setVisible(True)
            self.repeat_off.setVisible(False)
            self.volume_button.controlLeft(self.repeat_one)
            self.next.controlRight(self.repeat_one)

        if repeat_state == 'off':
            self.repeat_all.setVisible(False)
            self.repeat_one.setVisible(False)
            self.repeat_off.setVisible(True)
            self.volume_button.controlLeft(self.repeat_off)
            self.next.controlRight(self.repeat_off)


if __name__ == '__main__':
    # make cache directory
    if not os.path.exists(cachepath):
        xbmc.log('Creating directory for cache:' + cachepath)
        os.makedirs(cachepath)

    # get token
    token = util.prompt_for_user_token(username, cachepath, client_id=client_id, client_secret=client_secret)
    if token:
        sp = spotipyControl.SpotipyControl(auth=token)
    else:
        xbmc.log('Can\'t get token for ' + username)

    # create the GUI
    gui = Main("connectcontrol-main.xml", addonpath)

    # create and start a separate thread for the looping process that updates the window
    t1 = Thread(target=updateWindow, args=("thread 1", gui))
    t1.setDaemon(True)

    # run everything
    t1.start()
    gui.doModal()

    # delete the gui and the worker thread
    windowopen = False
    del gui
    del t1
