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
from sty import fg, bg, ef, rs


def main(lights, brightness=False, rgb=False, spotify=False):
    last_hsv = (0, 0, 0)
    last_track = ""
    lights.log.debug("spotify_background is now running")
    last_off = time.time()
    while not lights.thread_kill:
        new_track = spotify.get_track_id()
        if (new_track != last_track or last_hsv == (0,0,0)) and spotify.is_playing() :
            new_hsv = spotify.get_color()
            g, b, r = lights.hsv_to_gbr(new_hsv)
            hsv_text_block = bg(r, g, b) + "HSV: " + str(new_hsv) + bg.rs
            lights.log.debug("spotify_background: {} - {}".format(spotify.get_track_title(), hsv_text_block))
            print(hsv_text_block)
            lights.smooth_transition(0, 87, last_hsv, new_hsv, 0.3)
            last_hsv = new_hsv
            last_track = new_track
        if not spotify.is_playing():
            if (time.time()-last_off) > 30 or last_hsv != (0,0,0):
                lights.log.debug("spotify_background: Nothing playing - hsv: (0, 0, 0)")
                lights.smooth_transition(0, 87, last_hsv, (0, 0, 0), 0.3)
                last_hsv = (0, 0, 0)
                last_off = time.time()
        lights.spotify_keep_alive()
        time.sleep(0.1)
    lights.thread_end("spotify_background")


if __name__ == '__main__':
    lights = leds.light_strip(is_receiver=True)
    main(lights)
