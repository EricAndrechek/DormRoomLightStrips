import leds
import time

lights = leds.light_strip()
count = 0
rgb = (0, 0, 255)

while True:
    firsts = []
    firsts.append(lights.loop_region_fill(count, count + 3, rgb, "l"))
    time.sleep(0.05)
    lights.set_pixel(firsts[1], (0, 0, 0))
    count = count + 1
