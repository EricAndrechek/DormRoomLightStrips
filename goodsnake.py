import leds
import time

lights = leds.light_strip()
count = 0
rgb = (0, 0, 255)

while True:
    start = lights.loop_region_fill(count, count + 4, rgb, "l")
    time.sleep(0.05)
    print(start)
    lights.set_pixel(start, (0, 0, 0))
    count = count + 1
