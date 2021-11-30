import leds
import time
import random

lights = leds.light_strip()
count = 0

while True:
    hue = random.random()
    for i in range(0, 44):
        lights.ceiling_set_pixel(i, (hue, 0.99, 0.99), "r", False)
        lights.ceiling_set_pixel(i, (hue, 0.99, 0.99), "l", False)
        lights.pixels.show()
        time.sleep(0.06)

    hue = random.random()
    for i in range(0, 44):
        lights.ceiling_set_pixel(44-i, (hue, 0.99, 0.99), "r", False)
        lights.ceiling_set_pixel(44-i, (hue, 0.99, 0.99), "l", False)
        lights.pixels.show()
        time.sleep(0.06)
