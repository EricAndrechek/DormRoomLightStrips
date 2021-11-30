import leds
import time

lights = leds.light_strip()

lights.off()

# start = int(input("Start at: "))
# end = int(input("End at: "))
# red = int(input("Red: "))
# green = int(input("Green: "))
# blue = int(input("Blue: "))
while True:
    lights.all_pixels(lights.correct_color(
        (int(input("R: ")), int(input("G: ")), int(input("B: ")))))
    time.sleep(2)
    lights.off()
