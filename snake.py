import leds
import time

lights = leds.light_strip()

while True:
    for i in range(31, 112):
        lights.region_fill(i, i+5, (0, 0, 255))
        time.sleep(0.01)