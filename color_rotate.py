import time
import random
import leds


def main(lights, speed=0.1):
    hue = 0
    while True:
        i = 0
        while i < 87:
            lights.ceiling_set_pixel(i, ((hue + i / 87) % 1, 0.99, 0.9))
            i = i + 1
        lights.update()
        time.sleep(speed if speed >= 0.001 else 0.001)
        num_at_time = 1 if speed >= 0.001 else 33
        hue = (hue + num_at_time / 87) % 1


if __name__ == '__main__':
    lights = leds.light_strip()
    speed = float(input("Speed: "))
    main(lights, speed)
