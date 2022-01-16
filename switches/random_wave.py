import sys
sys.path.append("../")
import time
import random
import leds


def main(lights):
    hue = 0
    start = 0
    while True:
        hue = (hue + 0.1 + 0.8 * random.random()) % 1
        start = round(87 * random.random())
        for i in range(0, 44):
            lights.ceiling_set_pixel(start + i, (hue, 0.9, 0.9))
            lights.ceiling_set_pixel(start - i, (hue, 0.9, 0.9))
            lights.update()
            time.sleep(0.05)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
