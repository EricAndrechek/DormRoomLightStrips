import leds
import time

lights = leds.light_strip()
count = 0

while True:
    firsts = []
    firsts.append(lights.ceiling_region_fill(count, count + 3, (0, 1, 1), "r"))
    firsts.append(lights.ceiling_region_fill(
        count + 43, count + 46, (0.5, 1, 1), "r"))
    firsts.append(lights.ceiling_region_fill(
        count + 22, count + 25, (0.25, 1, 1), "l"))
    firsts.append(lights.ceiling_region_fill(
        count - 22, count - 19, (0.75, 1, 1), "l"))
    time.sleep(0.05)
    for i in firsts:
        lights.set_pixel(i, (0, 0, 0))
    count = count + 1
