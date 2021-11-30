from colorsys import hsv_to_rgb
import leds
import time
import colorsys

lights = leds.light_strip()

lights.off()

# start = int(input("Start at: "))
# end = int(input("End at: "))
# red = int(input("Red: "))
# green = int(input("Green: "))
# blue = int(input("Blue: "))
while True:
    hsv = (float(input("H: ")), 0.999, 0.999)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    rgb = (256 * rgb[0], 256 * rgb[1], 256 * rgb[2])
    lights.all(hsv)
    time.sleep(2)
    lights.all_off()
