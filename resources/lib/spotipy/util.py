
# shows a user's playlists (need to be authenticated via oauth)

from __future__ import print_function
from . import oauth2
import webbrowser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import threading
from time import sleep


class TokenHandler(BaseHTTPRequestHandler):
    global params
    params = False

    def do_GET(self):
        global params

        print("Just received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write('You may close the browser now!')

        parsed_path = urlparse.urlparse(self.path)
        try:
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params = {}

        return

    def log_request(self, code=None, size=None):
        pass

    def log_message(self, format, *args):
        print('Message')


def prompt_for_user_token(username, cachepath=None, scope=None, client_id=None,
                          client_secret=None, redirect_uri=None):
    redirect_uri = 'http://localhost:12345/'
    scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-follow-modify user-follow-read user-library-read user-library-modify user-read-private user-read-email user-read-birthdate user-top-read'
    if not cachepath:
        cachepath = ".cache-" + username

    # request the token
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope, cache_path=cachepath + '/' + username + '.cache')

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()

    if not token_info:

        server = HTTPServer(('localhost', 12345), TokenHandler)
        t = threading.Thread(target=server.handle_request)
        t.deamon = True
        t.start()

        auth_url = sp_oauth.get_authorize_url()
        try:
            webbrowser.open(auth_url)
            print("Opened %s in your browser" % auth_url)
        except:
            print("ConnectControl: Please navigate here: %s" % auth_url)

        while not params:
            print('wait for token')
            sleep(1)

        token_info = sp_oauth.get_access_token(params['code'])
    # Auth'ed API request
    if token_info:
        return token_info['access_token']
    else:
        return None
