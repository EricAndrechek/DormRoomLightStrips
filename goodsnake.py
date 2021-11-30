import leds
import time

lights = leds.light_strip()

while True:
    count = 0
    lights.region_fill(count % 81 + 31, count % 81 + 36, (0, 0, 255))
    count = count + 1