import leds
import time

lights = leds.light_strip()

while True:
    for i in range(31, 118):
        lights.set_pixel(i, (0, 0, 255))
        time.sleep(0.1)
    lights.off()
