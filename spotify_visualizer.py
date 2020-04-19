import logging
logging.basicConfig()
logging.getLogger('spotipy').setLevel(logging.DEBUG)

import light_controller as lc
import spotipy
from credentials import CREDENTIALS
import json

#to do

#class that authenticates w spotify

#find current song playing

#have a method that syncronizes the song to the beats/bars/tatums

#parse the rhythm and turn that into some lights

class SpotifyVisualizer:
    
    def __init__(self):
        self.token = None
        self.sp = None 
        self.track = None

    def authenticate(self):
        scope = "user-library-read user-modify-playback-state user-read-currently-playing user-read-playback-state"
        #token = spotipy.util.prompt_for_user_token(CREDENTIALS["SPOTIFY_USERNAME"], scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"],
        #        client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"])

        manager = spotipy.oauth2.SpotifyOAuth(username=CREDENTIALS["SPOTIFY_USERNAME"], scope=scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"], client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"], cache_path="cached_spotify_token.txt")

        #self.token = CREDENTIALS["SPOTIFY_TOKEN"]
        self.sp = spotipy.Spotify(oauth_manager=manager)
        results = self.sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])
    
    def get_track(self):
        track_info = self.sp.current_user_playing_track()
        self.track = track_info["item"]["uri"]

    def get_track_analysis(self):
        if self.track is not None:
            print(len(json.dumps(self.sp.audio_analysis(self.track), indent=4)))

def main():

    visualizer = SpotifyVisualizer()
    visualizer.authenticate()
    visualizer.get_track()
    visualizer.get_track_analysis()
    
if __name__ == "__main__":
    main()
