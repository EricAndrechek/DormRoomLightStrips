import leds
import time
import random


def main(lights):
    while (True):
        hue = random.random()
        lights.all_off()
        time.sleep(0.12)
        lights.fill_region_by_name("main", (hue, 0.99, 0.99))
        lights.update()
        time.sleep(0.005)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
