import time
import random
import leds


def main(lights, speed=0.1):
    hue = 0
    while True:
        i = 0
        while i < 87:
            num_at_time = 1
            if speed < 0.001:
                num_at_time = 5
            for j in range(0, num_at_time):
                lights.ceiling_set_pixel(
                    i + j, ((hue + (i + j) / 87) % 1, 0.99, 0.9))
            i = i + num_at_time
        lights.update()
        time.sleep(speed)
        hue = (hue + 1 / 87) % 1


if __name__ == '__main__':
    lights = leds.light_strip()
    speed = float(input("Speed: "))
    main(lights, speed)
