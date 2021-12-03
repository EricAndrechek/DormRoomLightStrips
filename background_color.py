import leds
import spotify
import image_color_helper
import numpy as np
from io import BytesIO
import urllib.request
from PIL import Image
import time


def main(lights):
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
                helper = image_color_helper.SpotifyBackgroundColor(image)
                new_color = helper.best_color()
                print(new_color)
                hsv = lights.rgb_to_hsv(new_color)
                lights.ceiling_region_fill(0, 87, hsv)
                lights.update()
        time.sleep(2)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
