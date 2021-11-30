import leds
import time

lights = leds.light_strip()

for i in range(50):
    lights.off()
    time.sleep(0.12)
    lights.on()
    time.sleep(0.01)