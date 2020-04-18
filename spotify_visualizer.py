import light_controller as lc
import spotipy
from credentials import CREDENTIALS

#to do

#class that authenticates w spotify

#find current song playing

#have a method that syncronizes the song to the beats/bars/tatums

#parse the rhythm and turn that into some lights

class SpotifyVisualizer:
    
    def __init__(self):
        pass

    def authenticate(self):
        scope = "user-library-read user-modify-playback-state user-read-currently-playing user-read-playback-state"
        spotipy.util.prompt_for_user_token(CREDENTIALS["SPOTIFY_USERNAME"], scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"],
                client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"])



def main():

    visualizer = SpotifyVisualizer()
    visualizer.authenticate()

if __name__ == "__main__":
    main()
