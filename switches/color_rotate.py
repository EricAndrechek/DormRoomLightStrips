# Friendly name: Color Rotate
# Internal name: color_rotate
# Brightness slider: True
# Brightness slider max: 99
# RGB: False
# Description: Rotates

import sys
sys.path.append("../")
sys.path.append("/home/pi/DormRoomLightStrips/")
import time
import random
import leds


def main(lights, brightness=False, rgb=False):
    hue = 0
    if brightness == 0:
        brightness = 1
    wait_time = 1 / brightness / 5
    while not lights.kill_thread:
        i = 0
        while i < 87:
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
            i = i + 1
        lights.update()
        time.sleep(wait_time)
        hue = (hue + 1 / 87) % 1
    lights.states[lights.thread]["state"] = 0
    lights.thread = None


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
