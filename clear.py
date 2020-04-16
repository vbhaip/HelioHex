import board
import neopixel

HEX_COUNT = 8 
LED_HEX = 36

BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(board.D18, HEX_COUNT*LED_HEX, auto_write=False)

for i in range(0, HEX_COUNT*LED_HEX):
    pixels[i] = BLACK
pixels.show()
