import leds
import time

lights = leds.light_strip()
count = 0

while True:
    firsts = []
    firsts.append(lights.ceiling_region_fill(
        count, count + 4, (0, 0.9, 0.9), "r"))
    firsts.append(lights.ceiling_region_fill(
        count + 43, count + 47, (0.5, 0.9, 0.9), "r"))
    firsts.append(lights.ceiling_region_fill(
        count + 22, count + 26, (0.25, 0.9, 0.9), "l"))
    firsts.append(lights.ceiling_region_fill(
        count - 22, count - 18, (0.75, 0.9, 0.9), "l"))

    for i in firsts:
        lights.set_pixel(i, (0, 0, 0))
    lights.update()
    time.sleep(0.05)
    count = count + 1
