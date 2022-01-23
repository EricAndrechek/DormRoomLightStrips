# Friendly name: Color Strobe
# Internal name: color_strobe
# Brightness slider: False
# Brightness slider max: 99
# RGB: False
# Description: strobes color

import sys
sys.path.append("../")
import leds
import time
import random


def main(lights, brightness=False, rgb=False):
    while (True):
        hue = random.random()
        lights.all_off()
        time.sleep(0.12)
        lights.fill_region_by_name("main", (hue, 0.99, 0.99))
        lights.update()
        time.sleep(0.005)


if __name__ == '__main__':
    arguments = sys.argv
    lights = leds.light_strip(is_receiver=True)
    main(lights)
