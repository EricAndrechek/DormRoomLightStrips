import leds
import time

lights = leds.light_strip()
count = 1000
rgb = (0,0,255)
while True:
    start = 31 + count % 86
    end = start + 5
    if (end > 117):
        end = end - 86\
    if (end > start and end != 117):
        lights.region_fill(start, end, rgb)
    if (end > start and end == 117):
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
    else:
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
        lights.region_fill(104, end)
    time.sleep(0.05)
    lights.set_pixel(end, (0,0,0))
    count = count - 1
    