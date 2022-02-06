import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D12, 117, auto_write=False, pixel_order=neopixel.GRB)

while True:
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(5)
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(5)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(5)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(5)
    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(5)
    pixels.fill((255, 0, 255))
    pixels.show()
    time.sleep(5)
    pixels.fill((0, 255, 255))
    pixels.show()
    time.sleep(5)
    pixels.fill((255, 255, 255))
    pixels.show()
    time.sleep(5)

