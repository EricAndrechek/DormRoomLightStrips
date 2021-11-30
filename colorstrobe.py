import leds
import time
import random

lights = leds.light_strip()

for i in range(50):
    color = (0,0,0)
    choice = random.random()
    rand = random.random()*255
    if (choice < 0.33):
        rand = random.random()*255
        color = (rand, 1 - rand, 0)
    if (choice >= 0.33 and choice < 0.67):
        color = (rand, 0, 1 - rand)
    if (choice >= 0.67):
        color = (0, rand, 1 - rand)
    lights.off()
    time.sleep(0.12)
    lights.region_fill(31, 118, color)
    time.sleep(0.01)