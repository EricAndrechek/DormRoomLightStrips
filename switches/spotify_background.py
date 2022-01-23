# Friendly name: Match Spotify Color
# Internal name: spotify_background
# Brightness slider: False
# Brightness slider max: 255
# RGB: False
# Description: Matches all lights to spotify background

import sys
sys.path.append("../")
import leds
import spotify
import time


def main(lights, brightness=False, rgb=False):
    last_hsv = (0, 0, 0)
    last_url = ""
    while True:
        url = spotify.spotify.get_current_track_url()
        if spotify.spotify.is_playing() and url != last_url:
            new_color = spotify.spotify.get_color()
            hsv = lights.rgb_to_hsv(new_color)
            lights.smooth_transition(0, 87, last_hsv, hsv, 0.3)
            last_url = url
            last_hsv = hsv
        time.sleep(2)


if __name__ == '__main__':
    lights = leds.light_strip(is_receiver=True)
    main(lights)
