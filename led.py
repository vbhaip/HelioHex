import board
import neopixel
from time import sleep

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


hexagons = [Hexagon(LED_HEX*x, LED_HEX*x + LED_HEX) for x in range(0, HEX_COUNT)] 

#hexagons[0].wave(ORANGE, 5, 0.2)
hexagons[0].rainbow_cycle(.01);
#hexagons[0].set_color(RED)
#sleep(5)
hexagons[0].set_color(BLACK)
