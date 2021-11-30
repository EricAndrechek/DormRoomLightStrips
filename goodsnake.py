import leds
import time

lights = leds.light_strip()
count = 0
rgb = (0,0,255)
while True:
    start = 104 + count % 87
    if (start > 117):
        start = start - 87
    end = start + 5
    if (end > 117):
        end = end - 87
    if (end > start and end != 117):
        lights.region_fill(start, end, rgb)
    if (end > start and end == 117):
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
    if (end < start):
        lights.region_fill(start, 116, rgb)
        lights.set_pixel(117, rgb)
        lights.region_fill(104, end)
    time.sleep(0.1)
    lights.set_pixel(end, (0,0,0))
    count = count - 1
    