import time
import leds
import os
import sys

p = os.path.abspath('.')
sys.path.insert(1, p)


def main(lights):
    while True:
        lights.off()
        time.sleep(0.12)
        lights.on()
        time.sleep(0.005)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
