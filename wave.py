import leds
import time
import random

lights = leds.light_strip()
count = 0
hue = 0
while True:
    hue = (hue + random.randrange(0.25, 0.75)) % 1
    start = (start + round(random.randrange(22, 66))) % 87
    for i in range(0, 44):
        lights.ceiling_set_pixel(start + i, (hue, 0.99, 0.99), "r", False)
        lights.ceiling_set_pixel(start - i, (hue, 0.99, 0.99), "r", False)
        lights.pixels.show()
        time.sleep(0.1)
