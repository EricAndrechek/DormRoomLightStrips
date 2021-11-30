import leds
import time
import random

lights = leds.light_strip()

while True:
    color = (random.randrange(0, 255), random.randrange(
        0, 255), random.randrange(0, 255))
    color2 = (random.randrange(0, 255), random.randrange(
        0, 255), random.randrange(0, 255))
    for i in range(31, 118):
        lights.set_pixel(i, color)
        time.sleep(0.1)
    for i in range(31, 118):
        lights.set_pixel(i, color2)
        time.sleep(0.1)
