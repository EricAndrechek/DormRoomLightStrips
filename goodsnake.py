import leds
import time

lights = leds.light_strip()
count = 0
while True:
    lights.loop_region_fill(count, count + 5, (0, 0, 255))
    time.sleep(0.1)
    lights.set_pixel(count, (0,0,0))
    count = count + 1
    