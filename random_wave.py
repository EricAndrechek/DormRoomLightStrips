import time
import random
import leds


def main(lights):
    while True:
        hue = (hue + 0.25 + 0.5 * random.random()) % 1
        start = (start + 22 + round(43 * random.random())) % 87
        for i in range(0, 44):
            lights.ceiling_set_pixel(start + i, (hue, 0.9, 0.9))
            lights.ceiling_set_pixel(start - i, (hue, 0.9, 0.9))
            lights.update
            time.sleep(0.1)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
