# Friendly name: Beat Spotify Lights
# Internal name: spotify_lights_beat
# Brightness slider: True
# Brightness slider max: 5
# RGB: False
# Description: spotify lights by beat

import sys

from spotify.pattern import Spotify_patterns
sys.path.append("../")
from time import time
import leds


def main(lights, brightness=1, rgb=False, spotify=False):
    spotty = Spotify_patterns(lights, brightness, rgb, spotify, "beat")
    spotty.runner()


if __name__ == '__main__':
    arguments = sys.argv
    brightness = int(arguments[1])
    lights = leds.light_strip(is_receiver=True)
    main(lights, brightness)
