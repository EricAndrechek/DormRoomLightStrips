import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D10, 117, auto_write=False, pixel_order=neopixel.GRB)

for i in range(117):
    print("----{}----".format(i))
    pixels[i] = (0, 255, 0)
    pixels.show()
    input("That was red")
    pixels[i] = (255, 0, 0)
    pixels.show()
    input("That was green")
    pixels[i] = (0, 0, 255)
    pixels.show()
    input("That was blue")
    pixels[i] = (0, 0, 0)
    pixels.show()
