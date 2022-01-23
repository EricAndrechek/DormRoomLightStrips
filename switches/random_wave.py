# Friendly name: Random Wave
# Internal name: random_wave
# Brightness slider: True
# Brightness slider max: 100
# RGB: False
# Description: Waves random

import sys
sys.path.append("../")
import time
import random
import leds


def main(lights, brightness):
    wait_time = 1 / brightness * 2
    hue = 0
    start = 0
    while True:
        hue = (hue + 0.1 + 0.8 * random.random()) % 1
        start = round(87 * random.random())
        for i in range(0, 44):
            lights.ceiling_set_pixel(start + i, (hue, 0.9, 0.9))
            lights.ceiling_set_pixel(start - i, (hue, 0.9, 0.9))
            lights.update()
            time.sleep(wait_time)


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
