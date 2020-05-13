
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
import colorsys
import random

VERBOSE = True 

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
        self.should_sync = False

        self.track_info = None
        
        self.sp_refresh = False 
        self.should_refresh = True
        self.should_update_playback = False
        self.should_run_visualizer = True

        self.sp_play_pause = None

        self.pos_lock = Lock()
        
        self.key = None

        self.threads = []

        self.curr_pitch = np.empty(12)

    def authenticate(self):
        scope = "user-library-read user-modify-playback-state user-read-currently-playing user-read-playback-state user-modify-playback-state"

        #token = spotipy.util.prompt_for_user_token(CREDENTIALS["SPOTIFY_USERNAME"], scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"], client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"])

        manager = spotipy.oauth2.SpotifyOAuth(username=CREDENTIALS["SPOTIFY_USERNAME"], scope=scope, client_id=CREDENTIALS["SPOTIFY_CLIENT_ID"], client_secret=CREDENTIALS["SPOTIFY_CLIENT_SECRET"], redirect_uri=CREDENTIALS["SPOTIFY_REDIRECT_URI"], cache_path="cached_spotify_token.txt")

        self.sp = spotipy.Spotify(oauth_manager=manager)
        self.sp_refresh = spotipy.Spotify(oauth_manager=manager)
        self.sp_play_pause = spotipy.Spotify(oauth_manager=manager)
        results = self.sp.current_user_saved_tracks()
        #for item in results['items']:
        #    track = item['track']
        #    print(track['name'] + ' - ' + track['artists'][0]['name'])

    def show(self, info):
        print(json.dumps(info, indent=4))
    
    def stop(self):
        self.should_run_visualizer = False
        #self.sp_refresh = False
        #self.should_refresh = False
        #self.should_update_playback = False

        for t in self.threads:
            t.join()

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
        #f = interp_fxns[self.get_location_index(x, x_val)]

        return float(f(x_val))

    def get_location_index(self, array, element):
        ind = np.searchsorted(array, element) - 1
        return ind
    
    def get_current_track(self):
        curr = perf_counter()
        #self.track_info = self.sp.current_user_playing_track()
        self.track_info = self.sp.current_playback()
        if(self.track_info != None):

            temp_track = self.track_info['item']['uri']
            if self.track is None: 
                self.track = temp_track 
                self.get_track_analysis()
                self.should_sync = True
                self.should_update_playback = True

            #this deals with if we switch songs
            elif self.track != temp_track:
                self.should_sync = False
                self.should_refresh = False
                self.should_update_playback = False
                self.track = temp_track
                self.get_track_analysis()
                self.should_sync = True
                self.should_refresh = True
                self.should_update_playback = True

            #arbitrarily subtract 0.5 seconds bc spotify's playback is off usually, and 0.5 seconds seems like an average amount
            self.update_pos((self.track_info['progress_ms'])/1000 - 1 + perf_counter() - curr)
        else:
            print("Please play a song to start.\n")

    def continuous_refresh_spotify_data(self):
        while self.should_run_visualizer: 
            if self.should_refresh:
                self.get_current_track()
                sleep(2)
   
    def continuous_update_playback(self):
        while self.should_run_visualizer:
            if self.should_update_playback and self.track_info['is_playing']:
                self.sp_play_pause.pause_playback()
                #sleep(0.1)
                self.sp_play_pause.start_playback()

                for x in range(120):
                    if self.should_run_visualizer:
                       sleep(2)

    def get_track_analysis(self):
        if self.track is not None:
            #self.show(self.sp.audio_analysis(self.track)['segments'][0:2])
           
            features = self.sp.audio_features(self.track)[0]
            
            self.acoustic = features['acousticness']
            self.energy = features['energy']
            self.valence = features['valence']
            #print(self.track_info['item']['name'] + "\t acoust\t" + str(features['acousticness']) + " energy\t" + str(features['energy']) + " liveness\t" + str(features['liveness']) + " valence\t" + str(features['valence']))
            
            analysis = self.sp.audio_analysis(self.track)
            segments = analysis['segments']
            
            try:
                self.key = analysis['sections'][0]['key']
            except:
                self.key = 7

            self.refresh_rate = (60.0/analysis['track']['tempo'])/4.0
            #self.refresh_rate = 0.05 
           
            time_vals = []
            loudness_vals = []
            pitch_vals = []
            for segment in segments:
                if 'start' not in segment:
                    time_vals.append(0.0)
                else:
                    time_vals.append(segment['start'])

                if 'loudness_start' not in segment:
                    segment['loudness_start'] = -30.0
                if 'loudness_max' not in segment:
                    segment['loudness_max'] = segment['loudness_start']
               
                #look to average loudness based off timbre 
                loudness_vals.append(segment['timbre'][0])
                
                pitch_norm = np.array(segment['pitches'])
                #put more of a bias on higher values for pitch
                pitch_norm = np.power(pitch_norm, 3)
                pitch_norm = pitch_norm/np.sum(pitch_norm)

                pitch_vals.append(pitch_norm)

            self.time_vals = time_vals

            #normalization for loudness vals from 0 to 1
            loudness_vals = np.array(loudness_vals)
            loudness_vals = (loudness_vals - np.min(loudness_vals))/np.ptp(loudness_vals)
            loudness_vals = loudness_vals
            self.loudness_vals = loudness_vals

            self.time_vals, self.loudness_vals = self.interp(self.time_vals, self.loudness_vals)

            
            
            self.pitch_vals = []
            self.pitch_vals = np.array(pitch_vals)

    def get_rgb_interp_fxns(self, pitch_vals):
        
        pitch_vals = 255*pitch_vals
        #note to self: if hex_count is not divisible by 4, might run into issues
        #time_vals = [x for x in range(0, lc.HEX_COUNT, lc.HEX_COUNT//4)]
        time_vals = [lc.HEX_COUNT*x/(4.0 - 1) for x in range(0, 4)] 

        _, r_interp = self.interp(time_vals, pitch_vals[0:4], length=4)
        _, g_interp = self.interp(time_vals, pitch_vals[4:8], length=4) 
        _, b_interp = self.interp(time_vals, pitch_vals[8:12], length=4)
        
        return(r_interp[0], g_interp[0], b_interp[0])

   
    def get_color_from_rgb_interp(self, r, g, b, ind):
        r_val = 255-max(0, min(255, 100 + int(r(ind) - 200*(self.energy - 0.5 + self.valence))))
        g_val = 255-max(0, min(255, 100 + int(g(ind) - 200*self.acoustic)))
        b_val = 255-max(0, min(255, 100 + int(b(ind) - 500*max(0, 0.5-self.valence))))

        return (r_val, g_val, b_val)

    def set_display_pitch(self, pitch_vals, uniform=False):
        r, g, b = self.get_rgb_interp_fxns(pitch_vals)
        

        ind = self.key 
        threads = []
        
        for i in range(0, lc.HEX_COUNT):
            if uniform is False:
                ind = i
            self.display.randomized_hexagons[i].set_color(self.get_color_from_rgb_interp(r, g, b, ind + 0.5), show=False)
            #t = Thread(target=self.display.hexagons[i].fade, args=(self.display.hexagons[i].color, self.get_color_from_rgb_interp(r,g,b,ind), 5, self.refresh_rate/2))
            #threads.append(t)


        #for t in threads:
        #    t.start()
        #
        #for t in threads:
        #    t.join()

        if uniform is True:
            sleep(self.refresh_rate*2)

    def get_hue_from_pitch(self, pitch):
        #get value from 0 to 1 corresponding to the hue
        pitch = list(pitch)
        #print([i/12.0 for i in range(0, 12)])
        hue = np.random.choice([i/12.0 for i in range(0, 12)], 1, p=pitch) 
        #print(hue[0])
        return hue[0]

    def process_color(self, hue):
        light = 0.5
        satur = 1.0

        energy_rng = 1/12.0 * random.uniform(0, self.energy)
        hue += energy_rng

        raw_rgb = tuple([255*i for i in colorsys.hls_to_rgb(hue, light, satur)])

        return raw_rgb

    def display_pitch_on_prob(self, pos):
        #sample value to get container
        #set each hexagon to the color
        ind = self.get_location_index(self.time_vals, pos)
        curr_pitch = self.pitch_vals[ind]
        #print(curr_pitch)

        
        #if(not (self.curr_pitch==curr_pitch).all()):
        
        hex_copy = self.display.hexagons.copy()
        random.shuffle(hex_copy)
        hex_copy = hex_copy[0:lc.HEX_COUNT//3]
        for hexagon in hex_copy:
            hue = self.get_hue_from_pitch(curr_pitch)
            rgb = self.process_color(hue)
            hexagon.set_color(rgb, show=False)

            #self.curr_pitch = curr_pitch


    def sync(self):
        temp_rainbow = lc.RAINBOW
        temp_rainbow.extend(lc.RAINBOW[0:4])

        temp = 1
        while self.should_run_visualizer:
            if self.should_sync and self.track_info is not None and self.track_info['is_playing']:
                    
                curr = perf_counter()
                #self.get_current_track()
                #self.pos += (perf_counter() - curr)
                #print(len(self.time_vals))
                #print(len(self.loudness_vals))
                curr_loudness = self.get_value_from_interp(self.pos, self.time_vals, self.loudness_vals)
                if VERBOSE:
                    print("Pos: " + str(self.pos) + " Loudness: " + str(curr_loudness))
                

                if self.pos > self.track_info['item']['duration_ms']/1000.0 - 1.0:
                    curr_loudness = (self.track_info['item']['duration_ms']/1000.0 - self.pos)  

                self.display.set_brightness(curr_loudness)
                
                
                self.display_pitch_on_prob(self.pos)

                #curr_pitch = []
                #for i in range(0, 12):
                #    curr_pitch.append(self.pitch_vals[i](self.pos))
                #curr_pitch = np.array(curr_pitch)
                
                #t = Thread(target=self.set_display_pitch, args=([curr_pitch]))
                #t.start()

                #if(curr_loudness > .79):
                #    self.set_display_pitch(curr_pitch, uniform=True)
                #else:
                #    self.set_display_pitch(curr_pitch)

                #self.display.set_color(temp_rainbow[np.argmax(curr_pitch)])
                sleep(self.refresh_rate)
                self.update_pos(self.pos + 0*self.refresh_rate + 1*(perf_counter() - curr))
    
    def visualize(self):

        self.authenticate()
        self.get_current_track()
        #self.get_track_analysis()
 
        self.threads = []
        self.threads.append(Thread(target=self.continuous_refresh_spotify_data))
        self.threads.append(Thread(target=self.continuous_update_playback))
        self.threads.append(Thread(target=self.sync))
        
        for t in self.threads:
            t.start()

def main():

    visualizer = SpotifyVisualizer()
    visualizer.visualize()


if __name__ == "__main__":
    main()
