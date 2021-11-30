import leds
import time
import random

lights = leds.light_strip()
count = 0
hue = 0
start = 0
while True:
    hue = (hue + 0.25 + 0.5 * random.random()) % 1
    start = (start + 22 + round(43 * random.randrange())) % 87
    for i in range(0, 44):
        lights.ceiling_set_pixel(start + i, (hue, 0.99, 0.99), "r", False)
        lights.ceiling_set_pixel(start - i, (hue, 0.99, 0.99), "r", False)
        lights.pixels.show()
        time.sleep(0.1)
