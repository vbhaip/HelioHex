
#to get the url from spotipy printed to terminal if we need to authenticate
import logging
logging.basicConfig()
logging.getLogger('spotipy').setLevel(logging.INFO)

import light_controller as lc
import spotipy
from credentials import CREDENTIALS
import json
from scipy import interpolate
import numpy as np
from time import sleep
from threading import Thread

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
        self.pos = None
        self.display = lc.Structure()
        self.display.set_color(lc.RED)

        self.time_vals = None
        self.loudness_vals = None


    def authenticate(self):
        scope = "user-library-read user-modify-playback-state user-read-currently-playing user-read-playback-state"
        manager = spotipy.oauth2.SpotifyOAuth(username=CREDENTIALS["SPOTIFY_USERNAME"], scope=scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"], client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"], cache_path="cached_spotify_token.txt")

        self.sp = spotipy.Spotify(oauth_manager=manager)
        results = self.sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])

    def show(self, info):
        print(json.dumps(info, indent=4))
    
    def interp(self, x, y, length=4):
        
        new_x_vals = []
        interp_fxns = []
        for i in range(0, len(x) - (length - 1), length):
           new_x_vals.append(x[i])
           interp_fxns.append(interpolate.interp1d(x[i:i+length], y[i:i+length], kind='nearest', fill_value='extrapolate', assume_sorted=True))

        return np.array(new_x_vals), np.array(interp_fxns)
    
    def get_value_from_interp(self, x_val, x, interp_fxns):
        loc = np.searchsorted(x, x_val)
        f = interp_fxns[loc]

        return f(x_val)

    def get_current_track(self):
        track_info = self.sp.current_user_playing_track()
        self.track = track_info['item']['uri']
        self.pos = track_info['progress_ms']/1000 

    def get_track_analysis(self):
        if self.track is not None:
            self.show(self.sp.audio_analysis(self.track)['segments'][0])

            analysis = self.sp.audio_analysis(self.track)
            segments = analysis['segments']
            
            time_vals = []
            loudness_vals = []
            for segment in segments:
                time_vals.append(segment['start'])
                loudness_vals.append(segment['loudness_start'])
            
            #normalization for loudness vals from 0 to 1
            loudness_vals = np.array(loudness_vals)
            loudness_vals = (loudness_vals - np.min(loudness_vals))/np.ptp(loudness_vals)
            
            self.time_vals, self.loudness_vals = self.interp(time_vals, loudness_vals)
    
    def sync(self):
        while True:
            self.get_current_track()
            curr_loudness = self.get_value_from_interp(self.pos, self.time_vals, self.loudness_vals)
            print("Pos: " + str(self.pos) + " Loudness: " + str(curr_loudness))
            self.display.set_brightness(curr_loudness)
            sleep(1)
            

def main():

    visualizer = SpotifyVisualizer()
    visualizer.authenticate()
    visualizer.get_current_track()
    visualizer.get_track_analysis()
    visualizer.sync()


if __name__ == "__main__":
    main()
