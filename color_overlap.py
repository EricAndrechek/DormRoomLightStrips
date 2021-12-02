import time
import random
import leds


def main(lights, speed=0.1):
    hue = 0
    spot = 0
    while True:
        lights.ceiling_set_pixel(spot, (hue, 0.99, 0.99))
        hue = hue + 0.001
        spot = (spot + 1) % 87


if __name__ == '__main__':
    lights = leds.light_strip()
    speed = float(input("Speed: "))
    main(lights, speed)
