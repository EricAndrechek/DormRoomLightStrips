import leds
import spotify
import image_color_helper
import numpy as np
from io import BytesIO
import urllib.request
from PIL import Image
import time


def main(lights):
    last_hsv = (0,0,0)
    last_url = ""
    while True:
        url = ""
        if spotify.is_playing():
            url = spotify.get_album_image()
            if url is not None and url != "" and url != last_url:
                last_url = url
                print(url)
                image_bytes = BytesIO(urllib.request.urlopen(url).read())
                image = np.array(Image.open(image_bytes))
                helper = image_color_helper.SpotifyBackgroundColor(image,  image_processing_size=(100,100))
                new_color = helper.best_color()
                hsv = lights.rgb_to_hsv(new_color)
                lights.smooth_transition(0, 87, last_hsv, hsv, 1)
                last_hsv = hsv
        time.sleep(2)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
