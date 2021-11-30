import leds
import time

lights = leds.light_strip()
rgb = (0, 0, 255)

while True:
    start = input("Start: ")
    end = input("End: ")
    start = lights.loop_region_fill(start, end, rgb, "l")
    time.sleep(1.5)
    lights.off()
