# Friendly name: Color Rotate Overlap
# Internal name: color_overlap
# Brightness slider: True
# Brightness slider max: 99
# RGB: False
# Description: Rotates and overlaps

import sys
sys.path.append("../")
import time
import random
import leds


def main(lights, brightness=False, rgb=False):
    wait_time = 1 / brightness / 2
    hue = 0
    spot = 0
    lights.log.debug("color_overlap is now running")
    while not lights.thread_kill:
        lights.ceiling_set_pixel(spot, (hue, 0.99, 0.99))
        hue = hue + 0.001 % 1
        spot = (spot + 1) % 87
        time.sleep(wait_time)
        lights.update()
    lights.thread_end("color_overlap")


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
