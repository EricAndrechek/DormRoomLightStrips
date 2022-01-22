import board
import neopixel
import time

class raw_leds:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            board.D18, 118, auto_write=False, pixel_order=neopixel.GRB)
    def set_pixel(self, n, gbr):
        self.pixels[n] = gbr
    def update(self):
        self.pixels.show()