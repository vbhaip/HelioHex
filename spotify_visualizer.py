
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
from time import sleep, perf_counter, time
from threading import Thread, Lock
from datetime import datetime 

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
        self.pitch_vals = None
        
        self.refresh_rate = None

        self.track_info = None
        
        self.sp_refresh = None
        self.should_refresh = False
        
        self.sp_play_pause = None

        self.pos_lock = Lock()
        
    def authenticate(self):
        scope = "user-library-read user-modify-playback-state user-read-currently-playing user-read-playback-state user-modify-playback-state"
        manager = spotipy.oauth2.SpotifyOAuth(username=CREDENTIALS["SPOTIFY_USERNAME"], scope=scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"], client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"], cache_path="cached_spotify_token.txt")

        self.sp = spotipy.Spotify(oauth_manager=manager)
        self.sp_refresh = spotipy.Spotify(oauth_manager=manager)
        self.sp_play_pause = spotipy.Spotify(oauth_manager=manager)
        results = self.sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print(track['name'] + ' - ' + track['artists'][0]['name'])

    def show(self, info):
        print(json.dumps(info, indent=4))
    
    def update_pos(self, new_val):
        self.pos_lock.acquire()
        self.pos = new_val
        self.pos_lock.release()
        #print(self.pos)

    def interp(self, x, y, length=4):
        
        new_x_vals = []
        interp_fxns = []
        for i in range(0, len(x) - (length - 1), length):
           new_x_vals.append(x[i])
           interp_fxns.append(interpolate.interp1d(x[i:i+length], y[i:i+length], kind='cubic', fill_value='extrapolate', assume_sorted=True))

        return np.array(new_x_vals), np.array(interp_fxns)
    
    def get_value_from_interp(self, x_val, x, interp_fxns):
        loc = np.searchsorted(x, x_val)
        f = interp_fxns[loc-1]

        return f(x_val)
    
    def get_current_track(self):
        curr = perf_counter()
        self.track_info = self.sp.current_user_playing_track()
        temp_track = self.track_info['item']['uri']
        if self.track is None: 
            self.track = temp_track 

        #this deals with if we switch songs
        elif self.track != temp_track:
            self.should_sync = False
            self.track = temp_track
            self.get_track_analysis()
            self.should_sync = True

        #arbitrarily subtract 0.5 seconds bc spotify's playback is off usually, and 0.5 seconds seems like an average amount
        self.update_pos((self.track_info['progress_ms'])/1000 - 1 + perf_counter() - curr)

    def continuous_refresh_spotify_data(self):
        while self.should_refresh:
            self.get_current_track()
            sleep(2)
   
    def continuous_update_playback(self):
        while self.should_refresh:
            self.sp_play_pause.pause_playback()
            sleep(0.1)
            self.sp_play_pause.start_playback()
            sleep(60)


    def get_track_analysis(self):
        if self.track is not None:
            self.show(self.sp.audio_analysis(self.track)['segments'][0])

            analysis = self.sp.audio_analysis(self.track)
            segments = analysis['segments']
                        
            self.refresh_rate = (60.0/analysis['track']['tempo'])/10.0
           
           
            time_vals = []
            loudness_vals = []
            pitch_vals = []
            for segment in segments:
                time_vals.append(segment['start'])
                loudness_vals.append(segment['loudness_max']-segment['loudness_start'])
                pitch_vals.append(segment['pitches'])

            #normalization for loudness vals from 0 to 1
            loudness_vals = np.array(loudness_vals)
            loudness_vals = (loudness_vals - np.min(loudness_vals))/np.ptp(loudness_vals)
            loudness_vals = loudness_vals*.2+.2


            self.time_vals, self.loudness_vals = self.interp(time_vals, loudness_vals)
            
            self.pitch_vals = []
            for i in range(0, 12):
                temp = interpolate.interp1d(time_vals, [pitch_vals[a][i] for a in range(0, len(pitch_vals))], kind='cubic', fill_value='extrapolate', assume_sorted=True)
                self.pitch_vals.append(temp)
            
            self.pitch_vals = np.array(self.pitch_vals)

    def get_rgb_interp_fxns(self, pitch_vals):
        
        pitch_vals = 255*pitch_vals
        #note to self: if hex_count is not divisible by 4, might run into issues
        time_vals = [x for x in range(0, lc.HEX_COUNT, lc.HEX_COUNT//4)]
        _, r_interp = self.interp(time_vals, pitch_vals[0:4], length=4)
        _, g_interp = self.interp(time_vals, pitch_vals[4:8], length=4) 
        _, b_interp = self.interp(time_vals, pitch_vals[8:12], length=4)
        
        return(r_interp[0], g_interp[0], b_interp[0])
   
    def get_color_from_rgb_interp(self, r, g, b, ind):
        r_val = 255-max(0, min(255, int(r(ind))))
        g_val = 255-max(0, min(255, int(g(ind))))
        b_val = 255-max(0, min(255, int(b(ind))))

        return (r_val, g_val, b_val)

    def set_display_pitch(self, pitch_vals):
        r, g, b = self.get_rgb_interp_fxns(pitch_vals)

        for i in range(0, lc.HEX_COUNT):
            self.display.hexagons[i].set_color(self.get_color_from_rgb_interp(r, g, b, i), show=False)

    def sync(self):
        temp_rainbow = lc.RAINBOW
        temp_rainbow.extend(lc.RAINBOW[0:4])
        self.should_sync = True
        while self.should_sync:
            curr = perf_counter()
            #self.get_current_track()
            #self.pos += (perf_counter() - curr)
            curr_loudness = self.get_value_from_interp(self.pos, self.time_vals, self.loudness_vals)
            print("Pos: " + str(self.pos) + " Loudness: " + str(curr_loudness))
            if(curr_loudness < 0):
                curr_loudness = 0.1
            self.display.set_brightness(curr_loudness)

            curr_pitch = []
            for i in range(0, 12):
                curr_pitch.append(self.pitch_vals[i](self.pos))
            curr_pitch = np.array(curr_pitch)
            
            self.set_display_pitch(curr_pitch)
            #self.display.set_color(temp_rainbow[np.argmax(curr_pitch)])
            sleep(self.refresh_rate - (perf_counter() - curr))
            self.update_pos(self.pos + self.refresh_rate)
    
    def visualize(self):
        self.should_refresh = True

        threads = []
        threads.append(Thread(target=self.continuous_refresh_spotify_data))
        threads.append(Thread(target=self.continuous_update_playback))
        threads.append(Thread(target=self.sync))
        
        for t in threads:
            t.start()

def main():

    visualizer = SpotifyVisualizer()
    visualizer.authenticate()
    visualizer.get_current_track()
    visualizer.get_track_analysis()
    visualizer.visualize()


if __name__ == "__main__":
    main()
