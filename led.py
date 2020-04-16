import board
import neopixel
from time import sleep
import random 
from threading import Thread
from flask import Flask

app = Flask(__name__)

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

RAINBOW = [PINK, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, VIOLET]

pixels = neopixel.NeoPixel(board.D18, HEX_COUNT*LED_HEX, auto_write=False)


class Hexagon:
    
    
    """
    Creates a range from start_val inclusive to end_val not inclusive
    for pixels that would be controlled
    """
    def __init__(self, start_val, end_val):
        self.start = start_val
        self.end = end_val

        #lets me know what solid hexagon color it is rn
        self.color = None
    
    def get_deviant_color(self, steps):
        r_dev = int(random.uniform(-1*steps, steps))
        g_dev = int(random.uniform(-1*steps, steps))
        b_dev = int(random.uniform(-1*steps, steps))
      
        return (max(0, min(255, self.color[0]+r_dev)), max(0, min(255, self.color[1]+g_dev)), max(0, min(255, self.color[2]+b_dev)))
        
    def set_color(self, color, show=True):
        for x in range(self.start, self.end):
            pixels[x] = color
        if show:
            pixels.show()
        self.color = color 
    """
    Side value of 0 - 5, sets it all to one color
    """
    
    def set_side_color(self, side, color, show=True):
        for x in range(self.start+side*LED_HEX//6, self.start+(side+1)*LED_HEX//6):
            pixels[x] = color
        if show:
            pixels.show()


    def clear(self, show=True):
        for x in range(self.start, self.end):
            pixels[x] = BLACK 
        if show:
            pixels.show()

    def wave(self, color, width, delay):
        if width >= LED_HEX:
            return

        for x in range(self.start + width, self.end-width):
            for y in range(x-width, x+width+1):
                pixels[y] = tuple(h//10 for h in color)
            pixels[x] = color

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
                pixels[i] = self.wheel(pixel_index & 255)
            pixels.show()
            sleep(wait)

    def color_wipe(self, color, wait):
        for i in range(self.start, self.end):
            pixels[i] = color
            sleep(wait)
    
    #Fades entire hex from color 1 to color 2
    def fade(self, c1, c2, steps, delay):
        r_step = int((c2[0] - c1[0])/steps)
        g_step = int((c2[1] - c1[1])/steps)
        b_step = int((c2[2] - c1[2])/steps)
        
        delay = delay / steps

        new_color = c1
        
        self.set_color(c1)
        sleep(delay)

        for x in range(0, steps):
            new_color = (new_color[0] + r_step, new_color[1] + g_step, new_color[2] + b_step) 
            self.set_color(new_color)
            sleep(delay)


class Structure:

    def __init__(self):
        self.hexagons = [Hexagon(LED_HEX*x, LED_HEX*x + LED_HEX) for x in range(0, HEX_COUNT)]
    
    def light_in_order(self, color, wait):
        for hexagon in self.hexagons:
            hexagon.set_color(color)
            sleep(wait)
    
    def rainbow_light_in_order(self, wait):
        for i in range(0, HEX_COUNT):
            self.hexagons[i].set_color(RAINBOW[i])
            sleep(wait)

    def set_color(self, color):
       
        threads = []
       
        #using threads here doesn't seem to change it, there's still a little delay between hexs
        for hexagon in self.hexagons:
            t = Thread(target=hexagon.set_color, args=(color, False))
            threads.append(t)
        
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        pixels.show()
    
    def fade(self, c1, c2, steps, delay):
        r_step = int((c2[0] - c1[0])/steps)
        g_step = int((c2[1] - c1[1])/steps)
        b_step = int((c2[2] - c1[2])/steps)
        
        delay = delay / steps

        new_color = c1
        
        self.set_color(c1)
        sleep(delay)

        for x in range(0, steps):
            new_color = (new_color[0] + r_step, new_color[1] + g_step, new_color[2] + b_step) 
            self.set_color(new_color)
            sleep(delay)

 
    def cycle_through_rainbow(self):
        self.set_color(RED);

        for x in range(1, len(RAINBOW)):
            self.fade(RAINBOW[x-1], RAINBOW[x], 20, 2.5)

    def flash_around(self, wait):
        threads = []
        
        hex_copy = self.hexagons
        random.shuffle(hex_copy)
        for hexagon in hex_copy: 
            t = Thread(target=hexagon.fade, args=(hexagon.color, hexagon.get_deviant_color(50), 20, 2.5))
            t.start()
            threads.append(t)
            
            sleep(random.uniform(wait/2.0, wait))


        for t in threads:
            t.join()
       

    def flash_around_base(self, base_color, wait):
        self.set_color(base_color)
        sleep(wait)
        self.flash_around(wait)



@app.route("/")
def index():
    return "hello"



def main():
    app.run(host="0.0.0.0", port=5000)
    display = Structure()

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
