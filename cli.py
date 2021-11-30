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
    hsv = (input("H: "), input("S: "), input("V: "))
    lights.all_pixels(lights.correct_color(
        colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])))
    time.sleep(2)
    lights.off()
