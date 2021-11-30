import leds
import time
import random

lights = leds.light_strip()

while (True):
    color = (0,0,0)
    choice = random.random()
    rand = random.random()*255
    if (choice < 0.33):
        rand = random.random()*255
        color = (rand, 256 - rand, 0)
    if (choice >= 0.33 and choice < 0.67):
        color = (rand, 0, 256 - rand)
    if (choice >= 0.67):
        color = (0, rand, 256 - rand)
    lights.off()
    time.sleep(0.10)
    lights.region_fill(31, 116, color)
    lights.set_pixel(117, color)
    time.sleep(0.01)