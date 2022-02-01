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


def main(lights, brightness=False, rgb=False, spotify=False):
    lights.log.debug("color_strobe is now running")
    while not lights.thread_kill:
        hue = random.random()
        lights.ceiling_fill_all((0, 0, 0))
        lights.update()
        time.sleep(0.12)
        lights.ceiling_fill_all((hue, 0.99, 0.99))
        lights.update()
        time.sleep(0.005)
    lights.thread_end("color_strobe")


if __name__ == '__main__':
    arguments = sys.argv
    lights = leds.light_strip(is_receiver=True)
    main(lights)
