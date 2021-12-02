import time
import random
import leds


def main(lights):
    hue = 0
    while True:
        for i in range(0, 87):
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
        lights.update()
        time.sleep(0.1)
        hue = (hue + 1 / 87) % 1


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
