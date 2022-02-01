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
    last_track = ""
    lights.log.debug("spotify_background is now running")
    while not lights.thread_kill:
        new_track = spotify.get_track_id()
        if new_track != last_track and spotify.is_playing():
            new_hsv = spotify.get_color()
            lights.log.debug("spotify_background color update: {} - hsv: {}".format(spotify.get_track_title(), new_hsv))
            lights.smooth_transition(0, 87, last_hsv, new_hsv, 0.3)
            last_hsv = new_hsv
            last_track = new_track
        if not spotify.is_playing():
            lights.log.debug("spotify_background color update: Nothing playing - hsv: (0, 0, 0)")
            lights.smooth_transition(0, 87, last_hsv, (0, 0, 0), 0.3)
            last_hsv = (0, 0, 0)
        time.sleep(0.1)
    lights.thread_end("spotify_background")


if __name__ == '__main__':
    lights = leds.light_strip(is_receiver=True)
    main(lights)
