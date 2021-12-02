import time
import random
import leds


def main(lights, speed=0.1):
    hue = 0
    while True:
        for i in range(0, 87):
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
            i = i + 3 if speed < 0.001 else i
        lights.update()
        time.sleep(speed)
        hue = (hue + 1 / 87) % 1


if __name__ == '__main__':
    lights = leds.light_strip()
    speed = float(input("Speed: "))
    main(lights, speed)
