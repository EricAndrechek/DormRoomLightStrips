import leds
import time
import colorsys

lights = leds.light_strip()

hsv = (0, 1, 1)
while(True):
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    lights.loop_region_fill(0, 86, rgb, "r")
    time.sleep(0.01)
    hsv = (hsv[0] + 1, hsv[1], hsv[2])
