

import resources.lib.spotipy.util as util
import resources.lib.spotipyControl as spotipyControl
# import resources.lib.helpers as helpers
import time
from types import *

username = 'Halbstark1708'


if __name__ == '__main__':
    token = util.prompt_for_user_token(username, '/Users/nicolas')

    if token:
        sp = spotipyControl.SpotipyControl(auth=token)
        player = sp.get_player()
        print(player['device']['name'])

    else:
        print('Cant get token for', username)
