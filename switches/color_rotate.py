# Friendly name: Color Rotate
# Internal name: color_rotate
# Brightness slider: True
# Brightness slider max: 99
# RGB: False
# Description: Rotates

import sys
sys.path.append("../")
import time
import random
import leds
import threading


def main(lights, brightness, rgb=False):
    t = threading.currentThread()
    hue = 0
    wait_time = 1 / brightness / 5
    while getattr(t, "do_run", True):
        i = 0
        while i < 87:
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
            i = i + 1
        lights.update()
        time.sleep(wait_time)
        hue = (hue + 1 / 87) % 1


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
