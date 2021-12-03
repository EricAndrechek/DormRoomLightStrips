import leds
import time
import colorsys


def main(lights):
    hsv = (0, 0.999, 0.9)
    while(True):
        hsv = (hsv[0] + 0.001, hsv[1], hsv[2])
        lights.ceiling_region_fill(0, 87, hsv)
        lights.update()
        time.sleep(0.01)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
