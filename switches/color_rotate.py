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


def main(lights, brightness, rgb=False):
    hue = 0
    wait_time = 1 / brightness / 5
    while True:
        i = 0
        while i < 87:
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
            i = i + 1
        lights.update()
        time.sleep(wait_time)
        hue = (hue + 1 / 87) % 1


if __name__ == '__main__':
    arguments = sys.argv
    print(arguments)
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
