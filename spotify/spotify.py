import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json
# import image_color_helper
# import numpy as np
# from io import BytesIO
# import urllib.request
# from PIL import Image
import colorsys
import time


class Spotify_helper:
    def __init__(self, log):
        self.log = log
        data = open(
            '/home/pi/DormRoomLightStrips/spotify/.spotify-credentials.json', 'r')
        creds = json.load(data)

        auth_manager = SpotifyOAuth(
            client_id=creds["ClientID"],
            client_secret=creds["ClientSecret"],
            redirect_uri=creds["RedirectUrl"],
            scope=creds["Scope"],
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.track_id = None
        self.track_duration = None
        self.track_position = None
        self.current_track_data = None
        self.is_playing_bool = False
        self.real_update_time = False

        # bool to see if update should be running or not.
        # if bool is true, update as follows:
        # check roku api to see if it is spotify and is playing
        # if it is, update duration and such and run general update every 2 seconds or so
        # if the roku progress is within 5 seconds of the duration, get the next song in the queue and run the analysis code on it
        # if roku playback is on spotify but is stopped, run general update code every second or so to see what is happening
        # if roku duration does not match compared to when last checked, run general update code to refresh for potential new song
        # if roku is not on spotify or isnt working, run general update code every second or so to see what is happening
        # if bool is false, nothing is currently using spotify, so run general update code every 2 minutes to just get some data ready for a fast boot if spotify button is pressed
        self.used = True
        self.general_update()

    def update_daemon(self):
        while self.used:
            self.general_update()
            time.sleep(2)

    def general_update(self):
        # checks if music is currently playing and updates values
        # look into adding roku api to here so we can get lots of updates without rate limiting
        try:
            ct = self.sp.current_user_playing_track()
        except Exception as e:
            self.log.error(e)
            return False
        self.real_update_time = time.time()
        if ct is not None:
            self.is_playing_bool = ct['is_playing']
        else:
            self.is_playing_bool = False
        # self.log.debug("Spotify is playing: " + str(self.is_playing_bool))
        if self.is_playing_bool:
            self.track_id = ct['item']['id']
            self.track_duration = ct['item']['duration_ms'] / 1000
            self.track_position = ct['progress_ms'] / 1000
        else:
            self.track_id = False
            self.track_duration = False
            self.track_position = False
        self.current_track_data = ct

    def roku_data(self):
        # check roku to see if it is spotify and is playing
        # get playback position and duration
        try:
            response = requests.get(
                "http://192.168.1.45:8060/query/media-player", timeout=3.1)
            if response.status_code == 200:
                return False  # come back to this once I have time to figure out how to get the roku to send the data
        except:
            return False

    def current_track(self):
        # checks if playing and returns current track data
        return self.current_track_data if self.is_playing_bool else False

    def get_time_offset(self):
        # returns number of seconds since data last updated
        return time.time() - self.real_update_time

    def get_track_id(self):
        # returns the track id of the current track if something is playing, otherwise returns false
        return self.track_id if self.is_playing_bool else False

    def get_album_image(self):
        # returns the url to the smallest image of the album
        if self.is_playing_bool:
            last_item = len(
                self.current_track_data['item']['album']['images']) - 1
            album_image = self.current_track_data['item']['album']['images'][last_item]['url']
            return album_image
        else:
            return False

    def get_track_title(self):
        # returns the name of the current track
        return self.current_track_data['item']['name'] if self.is_playing_bool else False

    def get_playback_position(self):
        # returns the current playback position in milliseconds
        return self.track_position if self.is_playing_bool else False

    def get_song_duration(self):
        # returns the duration of the current track in milliseconds
        return self.track_duration / 1000 if self.is_playing_bool else False

    def get_audio_features(self):
        # return audio features of the current track (only run on new track, not constantly. this will rate limit)
        return self.sp.audio_features(self.track_id) if self.is_playing_bool else False

    def get_audio_analysis(self):
        # return audio analysis of the current track (only run on new track, not constantly. this will rate limit)
        return self.sp.audio_analysis(self.track_id) if self.is_playing_bool else False
    """ def private_get_image_color(self):
        # need to offload this to something else
        url = self.get_album_image()
        if url is not None and url != "" and url is not False:
            image_bytes = BytesIO(urllib.request.urlopen(url).read())
            image = np.array(Image.open(image_bytes))
            helper = image_color_helper.SpotifyBackgroundColor(image,  image_processing_size=(100,100))
            try:
                new_color = helper.best_color()
            except ValueError:
                return False
            return new_color
        return False """

    def private_get_lyrics_color(self):
        response = requests.get(
            "https://spotify-color.andrechek.com/get_color")
        if response.status_code == 200:
            color = response.text
            if 'rgb' in color:
                rgb = color.split('rgb(')[1].split(')')[0].split(', ')
                hsv = colorsys.rgb_to_hsv(
                    int(rgb[0]) / 256, int(rgb[1]) / 256, int(rgb[2]) / 256)
                return hsv
            elif '#' in color:
                hex = color.split('#')[1]
                r = int(hex[0:2], 16)
                g = int(hex[2:4], 16)
                b = int(hex[4:6], 16)
                hsv = colorsys.rgb_to_hsv(r / 256, g / 256, b / 256)
                return hsv
            else:
                self.log.error("Error on /get_color request: " + response.text)
                return False  # self.private_get_image_color()
        else:
            self.log.error("Error on /get_color request: " + response.text)
            return False  # self.private_get_image_color()

    def get_color(self):
        if self.is_playing_bool:
            color = self.private_get_lyrics_color()
            if color is False:
                # fallback color white
                color = (0, 0, .9)
            return color
        return (0, 0, 0)

    def is_being_used(self, val):
        self.used = val

    def is_playing(self):
        return self.is_playing_bool


if __name__ == '__main__':
    helper = Spotify_helper()
    print(helper.get_color())
