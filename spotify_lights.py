from time import time
import leds
import time
from spotify import get_audio_analysis, get_playback_position
import spotify
import image_color_helper
import numpy as np
from io import BytesIO
import urllib.request
from PIL import Image
from cmath import sin, cos, phase, pi


def circular_average(inputs):
    sum = 0
    for x in inputs:
        sum = sum + complex(cos(2 * pi * x), sin(2 * pi * x))
    return phase(sum) / (2 * pi)


def get_beats_info():
    analysis = get_audio_analysis()
    beats = analysis["beats"]
    segments = analysis["segments"]
    spot = 0
    loudness = 0
    pitch = 0
    spot_length = len(segments)
    for beat in beats:
        loudnesses = []
        pitches = []
        segments_count = 0
        while spot < spot_length and segments[spot]["start"] < beat["start"] + beat["duration"]:
            loudnesses.append(segments[spot]["loudness_max"])
            for pitch in segments[spot]["pitches"]:
                pitches.append(pitch)
            segments_count = segments_count + 1
            spot = spot + 1
        loudness_avg = 0
        if segments_count > 0:
            for l in loudnesses:
                loudness_avg = loudness_avg + l / segments_count
            loudness = loudness_avg
            pitch = circular_average(pitches)
        beat["loudness"] = loudness
        beat["pitch"] = pitch
    return beats


def wave1(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    loudness = (beat["loudness"] - min_loudness) / \
        (max_loudness - min_loudness)
    distance = int(loudness * 30)
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    lights.ceiling_region_fill(0, 3, hsv, "r")
    lights.ceiling_region_fill(0, 3, hsv, "l")
    lights.update()
    for i in range(3, distance):
        lights.ceiling_set_pixel(i, hsv, "r")
        lights.ceiling_set_pixel(i, hsv, "l")
        lights.update()
        time.sleep(duration / 8 / distance)
    for i in range(distance - 1, 2, -1):
        if time.time() > start_time + beat["start"] + beat["duration"] - 0.2:
            lights.ceiling_region_fill(3, 84, (0, 0, 0))
            lights.update()
            break
        lights.ceiling_set_pixel(i, (0, 0, 0), "r")
        lights.ceiling_set_pixel(i, (0, 0, 0), "l")
        lights.update()
        time.sleep(duration / 3 / distance)


active_beats = []


def update_active_beats():
    for b in active_beats:
        if (b[3] > 43):
            active_beats.remove(b)
            continue
        lights.ceiling_set_pixel(b[3], (0, 0, 0), "r")
        lights.ceiling_set_pixel(b[3], (0, 0, 0), "l")
        b[3] = b[3] + 1
        if (b[3] + b[2] <= 43):
            lights.ceiling_set_pixel(b[3] + b[2], b[1], "r")
            lights.ceiling_set_pixel(b[3] + b[2], b[1], "l")


def wave2(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    loudness = (beat["loudness"] - min_loudness) / \
        (max_loudness - min_loudness)
    length = 3 + int(loudness * 4)
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    for i in range(0, 5):
        lights.ceiling_set_pixel(i, hsv, "r")
        lights.ceiling_set_pixel(i, hsv, "l")
        update_active_beats()
        lights.update()
        time.sleep(duration / 20)
    active_beats.append((0, hsv, length, 0))
    for i in range(0, 5):
        update_active_beats()
        lights.update()
        time.sleep(duration / 20)


def main(lights):
    adjust_hue = True
    last_url = ""
    while True:
        url = ""
        album_hue = 0
        if spotify.is_playing():
            if adjust_hue:
                url = spotify.get_album_image()
                if url is not None and url != "" and url != last_url:
                    last_url = url
                    print(url)
                    image_bytes = BytesIO(
                        urllib.request.urlopen(url).read())
                    image = np.array(Image.open(image_bytes))
                    helper = image_color_helper.SpotifyBackgroundColor(
                        image, image_processing_size=(100, 100))
                    new_color = helper.best_color()
                    hsv = lights.rgb_to_hsv(new_color)
                    album_hue = hsv[0]

            track = spotify.get_audio_features()[0]["id"]
            min_loudness = 0
            max_loudness = 0
            hues = []
            beats = get_beats_info()
            print(beats)
            for beat in beats:
                if beat["loudness"] < min_loudness:
                    min_loudness = beat["loudness"]
                if beat["loudness"] > max_loudness:
                    max_loudness = beat["loudness"]
                hues.append(beat["pitch"])
            avg_hue = circular_average(hues)
            if adjust_hue:
                hue_shift = album_hue - avg_hue
            else:
                hue_shift = 0
            start_time = time.time() - get_playback_position() + 0.5
            index = 0
            for beat in beats:
                while time.time() < start_time + beat["start"]:
                    continue
                if time.time() - start_time - beat["start"] > 0.5:
                    print("skip")
                    continue
                print(beat)
                """ if index % 10 == 0:
                    stopped = False
                    while not spotify.is_playing():
                        time.sleep(0.5)
                        stopped = True
                    if stopped:
                        start_time = time.time() - get_playback_position() - 1.5
                if index % 10 == 5:
                    if spotify.get_audio_features()[0]["id"] != track:
                        break """
                duration = start_time + \
                    beat["start"] + beat["duration"] - time.time()
                if duration > beat["duration"]:
                    duration = beat["duration"]
                print(time.time() - start_time - beat["start"])
                print(duration)
                if duration > 0:
                    wave2(lights, beat, start_time, duration,
                          min_loudness, max_loudness, hue_shift)
                else:
                    print("skip")
                index = index + 1
        time.sleep(1)


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
