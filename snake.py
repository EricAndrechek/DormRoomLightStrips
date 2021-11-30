import leds
import time

lights = leds.light_strip()

while True:
    for i in range(31, 113):
        lights.set_pixel(i, (0, 0, 255))
        lights.set_pixel(i+1, (0, 0, 255))
        lights.set_pixel(i+2, (0, 0, 255))
        lights.set_pixel(i+3, (0, 0, 255))
        lights.set_pixel(i+4, (0, 0, 255))
        time.sleep(0.05)
        lights.set_pixel(i, (0, 0, 0))
