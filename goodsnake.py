import leds
import time

lights = leds.light_strip()
count = 0
rgb = (0, 0, 255)

while True:
    firsts = []
    firsts.append(lights.loop_region_fill(count, count + 3, (0, 0, 255), "r"))
    firsts.append(lights.loop_region_fill(
        count + 43, count + 46, (50, 255, 0), "r"))
    firsts.append(lights.loop_region_fill(
        count + 22, count + 25, (255, 0, 0), "l"))
    firsts.append(lights.loop_region_fill(
        count - 22, count - 19, (0, 255, 255), "l"))
    time.sleep(0.05)
    for i in firsts:
        lights.set_pixel(i, (0, 0, 0))
    count = count + 1
