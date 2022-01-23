# Friendly name: UM Colors
# Internal name: umich_colors
# Brightness slider: False
# Brightness slider max: 100
# RGB: False
# Description: go blueee

import sys
sys.path.append("../")
import time
import random
import leds


def main(lights):
    blue = (0.583, 0.99, 0.4)
    maize = (0.18, 0.98, 0.99)
    while True:
        i = 0
        while True:
            for j in range(0, 87):
                if j % 8 <= 3:
                    lights.ceiling_set_pixel(i + j, blue)
                else:
                    lights.ceiling_set_pixel(i + j, maize)
            lights.update()
            time.sleep(0.1)
            i = i + 1


if __name__ == '__main__':
    arguments = sys.argv
    lights = leds.light_strip(is_receiver=True)
    main(lights)
