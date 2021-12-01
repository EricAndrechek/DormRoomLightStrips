import leds
import time
import random

lights = leds.light_strip()

while (True):
    hue = random.random()
    lights.all_off()
    time.sleep(0.12)
    lights.fill_region_by_name("main", (hue, 0.99, 0.99))
    lights.update()
    time.sleep(0.005)
