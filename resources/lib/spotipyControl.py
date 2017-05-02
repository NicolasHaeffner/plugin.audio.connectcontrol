from spotipy.client import Spotify


class SpotipyControl(Spotify):

    def __init__(self, auth=None, requests_session=True,
                 client_credentials_manager=None, proxies=None, requests_timeout=None):
        super(SpotipyControl, self).__init__(auth, requests_session,
                                             client_credentials_manager, proxies, requests_timeout)

    def get_devices(self):
        """ Get a User's Available Devices """
        return self._get('me/player/devices')

    def get_player(self):
        """ Get Information About The Users's Current Playback """
        return self._get('me/player')

    def get_currently_playing(self):
        """ Get the User's Currently Playing Track """
        return self._get('me/player/currently-playing')

    def put_player(self, device_id):
        """ Transfer a User's Playback NOT READY """
        return self._put('me/player', payload={'device_ids': [device_id], 'play': True})

    def pause(self):
        """Pause a User's Playback """
        return self._put('me/player/pause')

    def play(self):
        """ Start/Resume a User's Playback """
        return self._put('me/player/play')

    def next(self):
        """ Skip User's Playback To Next Track """
        return self._post('me/player/next')

    def previous(self):
        """ Skip User's Playback To Previous Track """
        return self._post('me/player/previous')

    def repeat(self, state):
        """ Set Repeat Mode On User's Playback

            Parameters:
                - state
                    track, context or off.
                    track will repeat the current track.
                    context will repeat the current context.
                    off will turn repeat off.
        """
        return self._put('me/player/repeat?state=' + state)

    def volume(self, volume_percent):
        """ Set Volume For User's Playback

            Parameters:
                - volume_percent (int)
                    The volume to set. Must be a value from 0 to 100 inclusive.
        """
        return self._put('me/player/volume?volume_percent=' + str(volume_percent))

    def shuffle(self, state):
        """ Toggle Shuffle For User's Playback

            Parameters:
                - state (Boolean)
                    True: Shuffle user's playback
                    False: Do not shuffle user's playback
        """
        return self._put('me/player/shuffle?state=' + str(state))

    def playContext(self, context_uri):
        """ Play Context (Valid contexts are albums, artists & playlists.)"""
        return self._put('me/player/play', payload={'context_uri': context_uri})

    def playTrack(self, uris):
        """ Play Array of Tracks defined by the uri"""
        if type(uris) is str:
            uris = [uris]
        return self._put('me/player/play', payload={'uris': uris})
