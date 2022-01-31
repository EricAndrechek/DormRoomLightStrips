# Friendly name: Cycle Colors
# Internal name: color_cycle
# Brightness slider: True
# Brightness slider max: 99
# RGB: False
# Description: Cycles full ceiling through RGB colors

import sys
sys.path.append("../")
import leds
import time
import colorsys


def main(lights, brightness=False, rgb=False):
    hsv = (0, 0.999, 0.9)
    if brightness == 0:
        brightness = 1
    wait_time = 1 / (brightness * brightness)
    lights.log.debug("color_cycle is now running")
    while not lights.thread_kill:
        hsv = (hsv[0] + 0.001, hsv[1], hsv[2])
        lights.ceiling_region_fill(0, 87, hsv)
        lights.update()
        time.sleep(wait_time)
    lights.states[lights.thread]["state"] = 0
    lights.log.debug("color_cycle has stopped")
    lights.thread = None


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
