# plugin.audio.connectcontrol

This addon provides a control frontend in Kodi for any kind of Spotify Connect enabled program, using the official webAPI from Spotify.

It is currently under development, so don't expect everything to work

## Screenshots

![alt text](https://picload.org/image/rcwpgiil/connectcontrol1.png)
![alt text](https://picload.org/image/rcwpgiii/connectcontrol2.png)

## Testing

if you want to test this addon, feel free to do so.
It is currently only tested under macOS and Ubuntu.
Here are some steps you have to take:

### Registering your Application at Spotify

You have to register your own App at Spotify:

1. Go to <https://developer.spotify.com/my-applications/#!/applications>
2. Chose a Application Name and a Application Description (can be something random)
3. The redirect URI depends, on whether you have a webbrowser installed on your system or not.
  * if you have a webbrowser installed, fill `http://localhost:12345/`.
  * if no webbrowser installed you have to use the (local) IP of your Kodi device instead of localhost. So `http://IP.OF.KODI:12345/`
4. Note down Client ID and Client Secret, you will need them later

### First Start

1. Before the fist start of the addon, you have to fill the Client ID, the Client Secret and your username into the settings of the addon.
2. Now it depends again if you have a browser available on the kodi device:
  * If you have a browser available start the addon. The browser should open with the prompt to login to spotify. If it is done (you will get a message to close the browser) you can close the browser and the addon should be ready.
  * If you don't have a browser available (for instance on libreelec) you have to do some more work:
    1. activate the debug log.
    2. run the addon.
    3. open the debug log and search for this: `ConnectControl: Please navigate here:` open this url on another device.
    4. login to spotify
    5. you should see a message stating 'You may close the browser now!'
    6. the addon should work like intended.
3. Enjoy :)

Make sure that you have a Spotify Programm running somewhere.
