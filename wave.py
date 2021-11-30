import leds
import time
import random

lights = leds.light_strip()
count = 0

while True:
    hue = random.random()
    start = round(random.randrange(0, 87))
    for i in range(0, 44):
        lights.ceiling_set_pixel(start + i, (hue, 0.99, 0.99), "r", False)
        lights.ceiling_set_pixel(start + i, (hue, 0.99, 0.99), "l", False)
        lights.pixels.show()
        time.sleep(0.1)
