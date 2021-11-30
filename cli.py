import leds
import time

lights = leds.light_strip()

lights.off()

# start = int(input("Start at: "))
# end = int(input("End at: "))
# red = int(input("Red: "))
# green = int(input("Green: "))
# blue = int(input("Blue: "))
lights.set_hex(input("Hex: "))
time.sleep(2)
lights.off()
time.sleep(2)
lights.on()