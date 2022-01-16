import sys
import time
import os

sys.path.append(os.path.abspath("/home/pi/DormRoomLights"))
from leds import light_strip

def main(lights):
    count = 0
    while True:
        firsts = []
        firsts.append(lights.ceiling_region_fill(
            count, count + 4, (0, 0.9, 0.9), "r"))
        firsts.append(lights.ceiling_region_fill(
            count + 43, count + 47, (0.5, 0.9, 0.9), "r"))
        if (count % 3 == 0):
            firsts.append(lights.ceiling_region_fill(
                int(count / 3) + 22, int(count / 3) + 26, (0.25, 0.9, 0.9), "l"))
            firsts.append(lights.ceiling_region_fill(
                int(count / 3) - 22, int(count / 3) - 18, (0.75, 0.9, 0.9), "l"))
        for i in firsts:
            lights.set_pixel(i, (0, 0, 0))
        lights.update()
        time.sleep(0.02)
        count = count + 1


if __name__ == '__main__':
    lights = light_strip()
    main(lights)
