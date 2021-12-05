import time
import random
import leds


def main(lights):
    blue = (0.583, 0.99, 0.4)
    maize = (0.133, 0.98, 0.99)
    while True:
        i = 0
        while True:
            for j in range(0, 87):
                if j % 8 <= 3:
                    lights.ceiling_set_pixel(i, blue)
                else:
                    lights.ceiling_set_pixel(i, maize)
            lights.update()
            time.sleep(0.1)
            i = i + 1


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
