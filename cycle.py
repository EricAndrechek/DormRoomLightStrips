import leds
import time
import colorsys

lights = leds.light_strip()

hsv = (0, 1, 1)
while(True):
    lights.loop_region_fill(0, 87, colorsys.hsv_to_rgb(hsv), "r")
    time.sleep(0.1)
    hsv = (hsv[0] + 1, hsv[1], hsv[2])
