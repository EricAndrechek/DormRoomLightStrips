# Friendly name: Strobe
# Internal name: strobe
# Brightness slider: False
# Brightness slider max: 99
# RGB: False
# Description: strobe

import sys
sys.path.append("../")
import time
import leds
import os
import sys


def main(lights, brightness=False, rgb=False):
    lights.log.debug("strobe is now running")
    while not lights.thread_kill:
        lights.off()
        time.sleep(0.12)
        lights.on()
        time.sleep(0.005)
    lights.thread_end("strobe")


if __name__ == '__main__':
    arguments = sys.argv
    lights = leds.light_strip(is_receiver=True)
    main(lights)
