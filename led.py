import board
import neopixel

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
BLACK = (255, 255, 255)

RAINBOW = [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]

PIXELS = neopixel.NeoPixel(board.D18, HEX_COUNT*LED_HEX, auto_write=False)


class Hexagon:
    

    """
    Creates a range from start_val inclusive to end_val not inclusive
    for pixels that would be controlled
    """
    def __init__(self, start_val, end_val):
        self.start = start_val
        self.end = end_val

    def set_color(self, color):
        for x in range(start, end):
            pixels[x] = color

        pixels.show()







