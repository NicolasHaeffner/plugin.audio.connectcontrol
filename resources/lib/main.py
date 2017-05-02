# -*- coding: utf-8 -*

import xbmcaddon
import xbmcgui
import os
import spotipyControl
import spotipy.util as util
import xbmc
import helpers

username = 'Halbstark1708'

# get addon info and set globals
addon = xbmcaddon.Addon()
addonpath = addon.getAddonInfo('path')


class Main(xbmcgui.WindowXML):

    def __init__(self, sp, *args, **kwargs):
        pass

    def onInit(self, sp):

        # definde controls
        self.cover = self.getControl(1001)
        self.cover.setImage(sp.get_player()['item']['album']['images'][0]['url'], False)
