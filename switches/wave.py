import leds
import time
import random

lights = leds.light_strip()
count = 0

while True:
    hue = random.random()
    for i in range(0, 87):
        