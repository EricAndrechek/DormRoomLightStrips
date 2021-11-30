import leds
import time
import colorsys

lights = leds.light_strip()

hsv = (0, 0.999, 0.999)
while(True):
    hsv = (hsv[0] + 0.001, hsv[1], hsv[2])
    lights.all(hsv)
    time.sleep(0.1)
