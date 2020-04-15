import board
import neopixel
from time import sleep
from random import random

HEX_COUNT = 1 
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

RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]

pixels = neopixel.NeoPixel(board.D18, HEX_COUNT*LED_HEX, auto_write=False)


class Hexagon:
    

    """
    Creates a range from start_val inclusive to end_val not inclusive
    for pixels that would be controlled
    """
    def __init__(self, start_val, end_val):
        self.start = start_val
        self.end = end_val

    def set_color(self, color):
        for x in range(self.start, self.end):
            pixels[x] = color

        pixels.show()
   
    """
    Side value of 0 - 5, sets it all to one color
    """
    
    def set_side_color(self, side, color):
        for x in range(self.start+side*LED_HEX/6, self.start+(side+1)*LED_HEX/6):
            pixels[x] = color
        pixels.show()


    def clear(self):
        for x in range(self.start, self.end):
            pixels[x] = BLACK 


    def wave(self, color, width, delay):
        if width >= LED_HEX:
            return

        for x in range(self.start + width, self.end-width):
            for y in range(x-width, x+width+1):
                pixels[y] = tuple(h//10 for h in color)
            pixels[x] = color

            pixels.show()
            sleep(delay)
            
            self.clear()

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
        
        
    #def flash_around_base(self, base_color, wait):
        

def main():
    hexagons = [Hexagon(LED_HEX*x, LED_HEX*x + LED_HEX) for x in range(0, HEX_COUNT)] 

    #hexagons[0].wave(ORANGE, 5, 0.2)
    hexagons[0].rainbow_cycle(.01);
    #hexagons[0].set_color(RED)
    #sleep(5)

    hexagons[0].fade(ORANGE, BLUE, 20, .25)
    hexagons[0].fade(BLUE, VIOLET, 20, .25)
    hexagons[0].fade(VIOLET, GREEN, 20, .25)
    hexagons[0].set_color(BLACK)

if __name__ == '__main__':
    main()
