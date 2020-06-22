import board
import neopixel
from time import sleep
import random 
from threading import Thread, Lock
from multiprocessing import Process
import signal
import sys
import structure_settings as settings
import randomcolor as rc
import datetime

dt = datetime.datetime

HEX_COUNT = 8 
LED_HEX = 36

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
VIOLET = (128, 0, 255)
PINK = (255, 0, 255)
BLACK = (0, 0, 0)

REFRESH_RATE = 0.001

RAINBOW = [PINK, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, VIOLET]

pixels = neopixel.NeoPixel(board.D18, HEX_COUNT*LED_HEX, auto_write=False, brightness=.5)


class Hexagon:
    
    
    """
    Creates a range from start_val inclusive to end_val not inclusive
    for pixels that would be controlled
    """
    def __init__(self, start_val, end_val, parent, offset = 0):
        self.start = start_val
        self.end = end_val

        #parent structure
        self.parent = parent
        self.hex_val = int(self.start/(LED_HEX))

        #lets me know what solid hexagon color it is rn
        self.color = None
    
        #used to see which hexagons connect to each other
        #will have to be adjusted manually depending on structure chosen
        #0 corresponds to bottom left side and 5 corresponds to bottom side
        self.connections = [None for i in range(0, 6)]
       
        
        self.offset = offset

        self.lock = Lock()
        
    def get_deviant_color(self, steps):
        r_dev = int(random.uniform(-1*steps, steps))
        g_dev = int(random.uniform(-1*steps, steps))
        b_dev = int(random.uniform(-1*steps, steps))
      
        return (max(0, min(255, self.color[0]+r_dev)), max(0, min(255, self.color[1]+g_dev)), max(0, min(255, self.color[2]+b_dev)))
    
    def adjust_pixel_index(self, val):
        return (((val-self.start)-6*self.offset)%36)+self.start
    
    def fix_color(self, color):
        #if max(color) <= 1:
        #    color = tuple([255*x for x in color])

        r = min(255, max(0, int(color[0])))
        g = min(255, max(0, int(color[1])))
        b = min(255, max(0, int(color[2])))
        return (r, g, b)

    def set_color(self, color, show=True):
        color = self.fix_color(color)
        self.lock.acquire()
        for x in range(self.start, self.end):
            pixels[x] = color

        self.lock.release()
        if show:
            pixels.show()
        self.color = color 
    """
    Side value of 0 - 5, sets it all to one color
    """
    
    def set_side_color(self, side, color, show=True, delay=0):
        for x in range(self.start+side*LED_HEX//6, self.start+(side+1)*LED_HEX//6):
            pixels[self.adjust_pixel_index(x)] = color
            sleep(delay)
        if show:
            pixels.show()


    def clear(self, show=True):
        for x in range(self.start, self.end):
            pixels[x] = BLACK 
        if show:
            pixels.show()
        self.color = BLACK

    def wave(self, color, width, delay):
        if width >= LED_HEX:
            return

        for x in range(self.start + width, self.end-width):
            for y in range(x-width, x+width+1):
                pixels[self.adjust_pixel_index(y)] = tuple(h//10 for h in color)
            pixels[self.adjust_pixel_index(x)] = color

            pixels.show()
            sleep(delay)
            
            self.clear(show=False)

    #From sample neopixel code
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
             r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) 

    #From sample neopixel code
    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.start, self.end):
                pixel_index = ((i-self.start) * 256 // LED_HEX) + j

                #bitwise AND, basically mod 256
                pixels[self.adjust_pixel_index(i)] = self.wheel(pixel_index & 255)
            #pixels.show()
            sleep(wait)

    def color_wipe(self, color, wait):
        for i in range(self.start, self.end):
            pixels[i] = color
            sleep(wait)
    
    #Fades entire hex from color 1 to color 2
    def fade(self, c1, c2, steps, delay, check_parent_process = False):
        r_step = int((c2[0] - c1[0])/steps)
        g_step = int((c2[1] - c1[1])/steps)
        b_step = int((c2[2] - c1[2])/steps)
        
        delay = delay / steps

        new_color = c1
        
        self.set_color(c1, show=False)
        sleep(delay)

        for x in range(0, steps):
            if(not check_parent_process or (check_parent_process and self.parent.continue_process)):
                new_color = (new_color[0] + r_step, new_color[1] + g_step, new_color[2] + b_step) 
                self.set_color(new_color, show=False)
                sleep(delay)

    def __repr__(self):
        return "Hexagon number: " + str(self.start/(LED_HEX))

class Structure:

    def __init__(self):
        self.hexagons = [Hexagon(LED_HEX*x, LED_HEX*x + LED_HEX, self) for x in range(0, HEX_COUNT)]
        
        self.randomized_hexagons = self.hexagons.copy()
        random.shuffle(self.randomized_hexagons)
        #print(self.randomized_hexagons)
        
        for key in settings.OFFSETS:
            self.hexagons[key].offset = settings.OFFSETS[key]
        #self.hexagons[1].offset = 5
        #self.hexagons[2].offset = 0
        #self.hexagons[3].offset = 4
        #self.hexagons[4].offset = 3
        #self.hexagons[5].offset = 0
        #self.hexagons[6].offset = 0
        #self.hexagons[7].offset = 2


        for item in settings.CONNECTIONS:
            self.connect(self.hexagons[item[0]], self.hexagons[item[1]], item[2])
        #self.connect(self.hexagons[1], self.hexagons[0], 0)
        #self.connect(self.hexagons[1], self.hexagons[3], 3)
        #self.connect(self.hexagons[1], self.hexagons[2], 4)
        #self.connect(self.hexagons[2], self.hexagons[3], 2) 
        #self.connect(self.hexagons[3], self.hexagons[4], 2)
        #self.connect(self.hexagons[3], self.hexagons[5], 3)
        #self.connect(self.hexagons[4], self.hexagons[5], 4)
        #self.connect(self.hexagons[5], self.hexagons[6], 4)
        #self.connect(self.hexagons[6], self.hexagons[7], 5)
        

        self.path = settings.PATH

        self.process = Thread(target=self.update, args=())
        
        self.process.start()
        
        self.continue_process = False


    def _continue_process(foo):
        def check(self, *args, **kwargs):
            if 'repeat' in kwargs and kwargs['repeat']:
                self.continue_process = True
            else:
                self.continue_process = False
            
            foo(self, *args, **kwargs)

            while self.continue_process:
                foo(self, *args, **kwargs)

        return check

    
    def clear(self):
        for hexagon in self.hexagons:
            hexagon.clear(show=False)
        pixels.show()

    def update(self):
        while True:
            pixels.show()
            sleep(REFRESH_RATE)

    def connect(self, hex1, hex2, hex1_side):
        hex1.connections[hex1_side] = hex2
        hex2.connections[(hex1_side+3)%6] = hex1
    
    def set_brightness(self, b):
        pixels.brightness = b
    
    def get_brightness(self):
        return pixels.brightness

    def ripple_fade(self, start_hex_ind, color, delay, fade_time):
        start_hex = self.hexagons[start_hex_ind] 
        hexagons_to_do = [start_hex]
        completed_hexagons = [] 
        while(len(hexagons_to_do) > 0):
            temp_hexagons_to_do = []
            processes = []
            while(len(hexagons_to_do) > 0):
                hexagon = hexagons_to_do.pop(0)
                t = Thread(target=hexagon.fade, args=(hexagon.color, color, 20, fade_time))
                processes.append(t) 
                
                completed_hexagons.append(hexagon)
                
                for connected_hexagon in hexagon.connections:
                    if connected_hexagon is not None and connected_hexagon not in completed_hexagons and connected_hexagon not in temp_hexagons_to_do:
                        temp_hexagons_to_do.append(connected_hexagon)
            
            for process in processes:
                process.start()
           
           # for process in processes:
           #     process.join()

            hexagons_to_do.extend(temp_hexagons_to_do) 

            sleep(delay)
        

    def light_in_order(self, color, wait):
        for hexagon in self.hexagons:
            hexagon.set_color(color, show=False)
            sleep(wait)
    
    def rainbow_light_in_order(self, wait):
        for i in range(0, HEX_COUNT):
            self.hexagons[i].set_color(RAINBOW[i], show=False)
            sleep(wait)

    def set_color(self, color):
       
        #should be of length HEX_COUNT 
        if isinstance(color, list):
            for i in range(0, HEX_COUNT):
                self.hexagons[i].set_color(color[i], show=False)
        
        else:
            #threads = []
           
            #using threads here doesn't seem to change it, there's still a little delay between hexs
            for hexagon in self.hexagons:
                hexagon.set_color(color, show=False)
                #t = Thread(target=hexagon.set_color, args=(color, False))
            #    threads.append(t)
            
            #for t in threads:
            #    t.start()

            #for t in threads:
            #    t.join()

        pixels.show()

    

    #note: added self.continue process check here, so it will only run this in continuous circumstances
    def fade(self, c1, c2, steps, delay):

        if(self.continue_process):
            r_step = int((c2[0] - c1[0])/steps)
            g_step = int((c2[1] - c1[1])/steps)
            b_step = int((c2[2] - c1[2])/steps)
            
            delay = delay / steps

            new_color = c1
            
            self.set_color(c1)
            sleep(delay)

            for x in range(0, steps):
                if(self.continue_process):
                    new_color = (new_color[0] + r_step, new_color[1] + g_step, new_color[2] + b_step) 
                    self.set_color(new_color)
                    sleep(delay)

    def fade_diff_hex(self, c1, c2, steps, delay):

        if(self.continue_process):
            threads = []

            for i in range(0, HEX_COUNT):
                threads.append(Thread(target=self.hexagons[i].fade, args=(c1[i], c2[i], steps, delay), kwargs={'check_parent_process': True}))

            for t in threads:
                t.start()

            for t in threads:
                t.join()


    @_continue_process 
    def cycle_through_rainbow(self, repeat=False):
        self.fade(RAINBOW[len(RAINBOW) - 1], RAINBOW[0], 20, 2.5);

        for x in range(1, len(RAINBOW)):
            if(self.continue_process):
                self.fade(RAINBOW[x-1], RAINBOW[x], 20, 2.5)

    @_continue_process
    def flash_around(self, wait, repeat=False):
        threads = []
        
        for hexagon in self.randomized_hexagons: 
            t = Thread(target=hexagon.fade, args=(hexagon.color, hexagon.get_deviant_color(50), 20, 2.5))
            t.start()
            threads.append(t)
            
            sleep(random.uniform(wait/2.0, wait))



        for t in threads:
            t.join()
       
    @_continue_process
    def flash_around_base(self, base_color, wait, repeat=True):
        self.set_color(base_color)
        sleep(wait)
        self.flash_around(wait)
    
    @_continue_process
    def rainbow_cycle(self, wait, repeat=False):
        threads = []

        for hexagon in self.hexagons:
            threads.append(Thread(target=hexagon.rainbow_cycle, args=[wait]))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def get_color_palette(self, hue=None):
        rand_color = rc.RandomColor()
        
        if hue is not None:
            p = rand_color.generate(count=HEX_COUNT, format_='rgb', hue=hue)
        else:
            p = rand_color.generate(count=HEX_COUNT, format_='rgb')

        p = [x[4:-1].split(",") for x in p]
        p = [tuple(int(x) for x in y) for y in p]

        return p

    def set_color_palette(self, hue=None):

        p = self.get_color_palette(hue=hue) 

        self.set_color(p)

        return p

    def first_time_day_sync(self):
        sunrise_hour = 6
        sunset_hour = 20 
        
        curr_hour = dt.now().hour
        next_hour = (curr_hour+1)%24

        if(sunrise_hour <= next_hour < sunset_hour):
            color = 'orange' if random.random() > 0.5 else 'yellow'
        else:
            color = 'blue' if random.random() > 0.5 else 'purple'

        self.set_color(self.get_color_palette(hue=color))
       

    @_continue_process
    def time_day_sync(self, repeat=False):

        sunrise_hour = 6
        sunset_hour = 20 
        
        curr_hour = dt.now().hour
        next_hour = (curr_hour+1)%24

        if(sunrise_hour <= next_hour < sunset_hour):
            color = 'orange' if random.random() > 0.5 else 'yellow'
        else:
            color = 'blue' if random.random() > 0.5 else 'purple'
       
        #for five min it switches between diff colors
        self.fade_diff_hex([i.color for i in self.hexagons], self.get_color_palette(hue=color), 100, 300)


    def light_border(self, color):
        for hexagon in self.hexagons:
            print(hexagon.connections)
            for i in range(0, 6):
                if hexagon.connections[i] is None:
                    hexagon.set_side_color(i, color, show = False)


    def chase_perimeter(self, color):

        curr_hex_ind = 0
        curr_side = 1
        
        curr_hex = self.hexagons[curr_hex_ind]
        while not (curr_hex_ind is 0 and curr_side is 0):
            if(curr_hex.connections[curr_side] is not None):
                curr_hex_ind = curr_hex.connections[curr_side].hex_val
                curr_side = (curr_side+3)%6
                curr_side = (curr_side+1)%6
                curr_hex = self.hexagons[curr_hex_ind]

            curr_hex.set_side_color(curr_side, color, delay=0.15/6)
            curr_side = (curr_side+1)%6

            #sleep(0.15)
    
    @_continue_process
    def rainbow_chase(self, repeat=False):
        for color in RAINBOW:
            if(self.continue_process):
                self.chase_perimeter(color)






def end_program(sig, frame):
    for i in range(0, LED_HEX*HEX_COUNT):
        pixels[i] = BLACK
    pixels.show()
    sys.exit(0)

def main():
    display = Structure()
    signal.signal(signal.SIGINT, end_program)

    while True:
        for a in RAINBOW:
            display.chase_perimeter(a)
            sleep(0) 

    display.set_color(YELLOW)
    display.rainbow_light_in_order(.5)


    for x in range(0, 5):
        for color in RAINBOW:
            t = Thread(target=display.ripple_fade, args=(5, color, .5, 1))
            t.start()
            sleep(2)
            
    for color in RAINBOW:
        display.ripple_fade(int(random.uniform(0, 6)), color, .5, 2)
    #display.ripple_fade(5, PINK, .4, .1)
    #display.ripple_fade(3, GREEN, .4, .1)
    #app.run(host="0.0.0.0", port=5000)

    #display.rainbow_light_in_order(.1)
    
    display.cycle_through_rainbow()

    display.set_color(BLACK)

    hexagons = display.hexagons
   
    display.flash_around_base(BLUE, 3)
    display.flash_around(3)
    display.flash_around(3)


    display.set_color(BLACK)
    
    #hexagons[0].wave(ORANGE, 5, 0.2)
    #hexagons[0].rainbow_cycle(.01);
    #hexagons[0].set_color(RED)
    #sleep(5)


if __name__ == '__main__':
    main()
