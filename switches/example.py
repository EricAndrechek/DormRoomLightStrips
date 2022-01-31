# Friendly name: Example # this is what will show up in homekit
# Internal name: example # this is the name of the file
# Brightness slider: True # if False, the brightness slider will not show up
# Brightness slider max: 255 # the maximum brightness value
# RGB: True # if False, the RGB wheel will not show up
# Description: This is an example of how to create a new switch - it provides no functionality

# all functional descriptions must go at the the top of the file as shown.
# all files need to take a brightness or led parameter as the maximum possible ways of inputting data into the switch and nothing more
# ie: if you want to control a speed of a pattern this switch will do out of 5 options, set Brightness slider to True, and set the slider max to 5.


import sys
sys.path.append("../")
import leds


def main(lights, brightness=False, rgb=False):
    lights.log.debug("example is now running")

    while not lights.thread_kill:
        # do whatever you want to put here
        pass

    lights.states["example"]["state"] = 0
    lights.log.debug("example has stopped")
    lights.thread = None

if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    r = arguments[2]
    g = arguments[3]
    b = arguments[4]
    rgb = (int(r), int(g), int(b))
    # change to is_transmitter=True if you want to be a transmitter
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness, rgb)
