import leds
import time

lights = leds.light_strip()
count = 0
while True:
    lights.set_pixel(count % 81 + 30, (0,0,0))
    lights.region_fill(count % 81 + 31, count % 81 + 36, (0, 0, 255))
    count = count + 1
    time.sleep(0.1)