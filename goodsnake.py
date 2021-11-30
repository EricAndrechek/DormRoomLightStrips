import leds
import time

lights = leds.light_strip()
count = 0
rgb = (0, 0, 255)
""" while True:
    start = 31 + count % 86
    end = start + 5
    if (end > 117):
        end = end - 86
    if (end > start and end != 117):
        lights.region_fill(start, end, rgb)
    elif (end > start and end == 117):
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
    else:
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
        lights.region_fill(104, end, rgb)
    time.sleep(0.05)
    lights.set_pixel(end, (0, 0, 0))
    if (end == 117):
        lights.set_pixel(31, (0, 0, 0))
    count = count - 1 """

while True:
    lights.loop_region_fill(count, count + 4, rgb, "r")
    start = 104 + count % 88
    if (start > 117):
        start = start - 87
    time.sleep(0.05)
    lights.set_pixel(start, (0, 0, 0))
    count = count + 1
