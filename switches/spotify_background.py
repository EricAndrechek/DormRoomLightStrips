# Friendly name: Match Spotify Color
# Internal name: spotify_background
# Brightness slider: False
# Brightness slider max: 255
# RGB: False
# Description: Matches all lights to spotify background

import sys
sys.path.append("../")
import leds
import time


def main(lights, brightness=False, rgb=False, spotify=False):
    last_hsv = (0, 0, 0)
    last_url = ""
    lights.log.debug("spotify_background is now running")
    while not lights.thread_kill:
        new_url = spotify.get_album_image()
        if new_url != last_url:
            rgb = spotify.get_color()
            new_hsv = lights.rgb_to_hsv(rgb)
            lights.log.debug("spotify_background: rgb: {} and hsv: {}".format(rgb, new_hsv))
            if new_hsv != last_hsv:
                lights.smooth_transition(0, 87, last_hsv, new_hsv, 0.3)
                last_hsv = new_hsv
            last_url = new_url
        time.sleep(0.1)
    lights.thread_end("spotify_background")


if __name__ == '__main__':
    lights = leds.light_strip(is_receiver=True)
    main(lights)
