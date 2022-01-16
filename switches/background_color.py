import sys
sys.path.append("../")
import leds
import spotify
import time


def main(lights):
    last_hsv = (0,0,0)
    last_url = ""
    while True:
        url = spotify.get_current_track_url()
        if spotify.is_playing() and url != last_url:
            new_color = spotify.get_color()
            hsv = lights.rgb_to_hsv(new_color)
            lights.smooth_transition(0, 87, last_hsv, hsv, 0.3)
            last_url = url
            last_hsv = hsv
        time.sleep(2)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
