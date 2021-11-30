import leds
import time
import colorsys

lights = leds.light_strip()

hsv = (0, 1, 1)
while(True):
    hsv = (hsv[0] + 0.01, hsv[1], hsv[2])
    time.sleep(0.1)
