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
import random


def circular_average(inputs):
    sum = 0
    for x in inputs:
        sum = sum + complex(cos(2 * pi * x), sin(2 * pi * x))
    return phase(sum) / (2 * pi)


def get_beats_info(division):
    analysis = get_audio_analysis()
    if division == "tatum":
        beats = analysis["tatums"]
    else:
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


def pattern1(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
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


state2 = []


def update_state2():
    for b in state2:
        if (b[3] > 43):
            state2.remove(b)
            continue
        lights.ceiling_set_pixel(b[3], (0, 0, 0), "r")
        lights.ceiling_set_pixel(b[3], (0, 0, 0), "l")
        b[3] = b[3] + 1
        if (b[3] + b[2] <= 43):
            lights.ceiling_set_pixel(b[3] + b[2], b[1], "r")
            lights.ceiling_set_pixel(b[3] + b[2], b[1], "l")


def pattern2(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    loudness = (beat["loudness"] - min_loudness) / \
        (max_loudness - min_loudness)
    if loudness != max_loudness:
        loudness = loudness ** 2
    length = 1 + int(loudness * 7)
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    for i in range(0, length + 1):
        lights.ceiling_set_pixel(i, hsv, "r")
        lights.ceiling_set_pixel(i, hsv, "l")
        update_state2()
        lights.update()
        time.sleep(duration / 30)
    state2.append([0, hsv, length, 0])
    for i in range(0, 5):
        update_state2()
        lights.update()
        time.sleep((i + 1) * duration / 30)


state3 = (0, (0, 0, 0))  # (center, hsv)


def pattern3(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    global state3
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    prev_start = state3[0] - 10
    prev_end = state3[0] + 10
    if beat["start"] == 0:
        center = random.randrange(0, 87)
    elif prev_start >= 0 and prev_end < 87:
        center = random.choice(
            list(range(0, prev_start + 1)) + list(range(prev_end, 87)))
    elif prev_end >= 87:
        center = random.randrange((prev_end) % 87, prev_start + 1)
    else:
        center = random.randrange(prev_end, prev_start % 87 + 1)
    lights.ceiling_set_pixel(center, hsv)
    lights.update()
    time.sleep(duration / 22)
    for i in range(1, 6):
        lights.ceiling_set_pixel(center + i, hsv)
        lights.ceiling_set_pixel(center - i, hsv)
        if beat["start"] != 0:
            lights.ceiling_set_pixel(state3[0] - 6 + i, (0, 0, 0))
            lights.ceiling_set_pixel(state3[0] + 6 - i, (0, 0, 0))
            lights.ceiling_region_fill(
                state3[0] - 5 + i, state3[0] + 5 - i, (state3[1][0], state3[1][1], 1 - i * 0.2))
        lights.update()
        time.sleep(duration / 22)
    lights.ceiling_set_pixel(state3[0], (0, 0, 0))
    lights.update()
    state3 = (center, hsv)


state4 = (0, 0, (0, 0, 0))   # (center, length, hsv)


def pattern4(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    global state4
    loudness = (beat["loudness"] - min_loudness) / \
        (max_loudness - min_loudness)
    if loudness != max_loudness:
        loudness = loudness ** 2
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    length = int(2 + 4 * loudness)
    if beat["start"] == 0:
        center = 0
    else:
        center = (state4[0] + state4[1] + length + 3) % 87

    if length >= state4[1]:
        for i in range(0, length + 1):
            lights.ceiling_set_pixel(center + i, hsv)
            lights.ceiling_set_pixel(center - i, hsv)

            lights.ceiling_set_pixel(center + i + 43, hsv)
            lights.ceiling_set_pixel(center - i + 43, hsv)

            if beat["start"] != 0 and i < state4[1]:
                lights.ceiling_set_pixel(
                    state4[0] - state4[1] + i, (0, 0, 0))
                lights.ceiling_set_pixel(
                    state4[0] + state4[1] - i, (0, 0, 0))
                lights.ceiling_region_fill(
                    state4[0] - state4[1] + i + 1, state4[0] + state4[1] - i - 1, (state4[2][0], state4[2][1], 1 - ((i + 1) / state4[1]) ** 2))
                if i == state4[1] - 1:
                    lights.ceiling_set_pixel(state4[0], (0, 0, 0))

                lights.ceiling_set_pixel(
                    state4[0] - state4[1] + i + 43, (0, 0, 0))
                lights.ceiling_set_pixel(
                    state4[0] + state4[1] - i + 43, (0, 0, 0))
                lights.ceiling_region_fill(
                    state4[0] - state4[1] + i + 1 + 43, state4[0] + state4[1] - i - 1 + 43, (state4[2][0], state4[2][1], 1 - ((i + 1) / state4[1]) ** 2))
                if i == state4[1] - 1:
                    lights.ceiling_set_pixel(state4[0] + 43, (0, 0, 0))
            lights.update()
            time.sleep(duration / 14)

    if length < state4[1]:
        for i in range(0, state4[1]):
            if i < length + 1:
                lights.ceiling_set_pixel(center + i, hsv)
                lights.ceiling_set_pixel(center - i, hsv)

                lights.ceiling_set_pixel(center + i + 43, hsv)
                lights.ceiling_set_pixel(center - i + 43, hsv)
            if beat["start"] != 0:
                lights.ceiling_set_pixel(
                    state4[0] - state4[1] + i, (0, 0, 0))
                lights.ceiling_set_pixel(
                    state4[0] + state4[1] - i, (0, 0, 0))
                lights.ceiling_region_fill(
                    state4[0] - state4[1] + i + 1, state4[0] + state4[1] - i - 1, (state4[2][0], state4[2][1], 1 - ((i + 1) / state4[1]) ** 2))
                if i == state4[1] - 1:
                    lights.ceiling_set_pixel(state4[0], (0, 0, 0))

                lights.ceiling_set_pixel(
                    state4[0] - state4[1] + i + 43, (0, 0, 0))
                lights.ceiling_set_pixel(
                    state4[0] + state4[1] - i + 43, (0, 0, 0))
                lights.ceiling_region_fill(
                    state4[0] - state4[1] + i + 1 + 43, state4[0] + state4[1] - i - 1 + 43, (state4[2][0], state4[2][1], 1 - ((i + 1) / state4[1]) ** 2))
                if i == state4[1] - 1:
                    lights.ceiling_set_pixel(state4[0] + 43, (0, 0, 0))
            lights.update()
            time.sleep(duration / 18)
    state4 = (center, length, hsv)


def pattern5(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift):
    hsv = ((beat["pitch"] + hue_shift) % 1, 0.99, 0.99)
    while time.time() < start_time - duration - 0.05:
        lights.ceiling_region_fill(0, 87, hsv)
        time.sleep(0.02)
        lights.ceiling_region_fill(0, 87, (0, 0, 0))
        time.sleep(0.02)


def light_pattern(lights, beat, start_time, duration, min_loudness, max_loudness, hue_shift, pattern):
    if pattern == 1:
        pattern1(lights, beat, start_time, duration,
                 min_loudness, max_loudness, hue_shift)
    elif pattern == 2:
        pattern2(lights, beat, start_time, duration,
                 min_loudness, max_loudness, hue_shift)
    elif pattern == 3:
        pattern3(lights, beat, start_time, duration,
                 min_loudness, max_loudness, hue_shift)
    elif pattern == 4:
        pattern4(lights, beat, start_time, duration,
                 min_loudness, max_loudness, hue_shift)
    elif pattern == 5:
        pattern5(lights, beat, start_time, duration,
                 min_loudness, max_loudness, hue_shift)


def main(lights):
    track = ""
    adjust_hue = True
    last_url = ""
    division = input("Division: ")
    pattern = input("Pattern: ")
    while True:
        url = ""
        album_hue = 0
        if spotify.is_playing():
            if adjust_hue:
                url = spotify.get_album_image()
                if url is not None and url != "" and url != last_url:
                    last_url = url
                    # print(url)
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
            beats = get_beats_info(division)
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
            start_time = time.time() - get_playback_position() + 0.3
            index = -1
            for beat in beats:
                index = index + 1
                while time.time() < start_time + beat["start"]:
                    continue
                if time.time() - start_time - beat["start"] > 0.5:
                    print("skip")
                    continue
                print("Beat " + str(index) + ": " + str(beat["start"]))
                """ if index % 10 == 0:
                    stopped = False
                    while not spotify.is_playing():
                        time.sleep(0.5)
                        stopped = True
                    if stopped:
                        start_time = time.time() - get_playback_position() + 0.3
                if index % 10 == 5:
                    if spotify.get_audio_features()[0]["id"] != track:
                        break """
                duration = start_time + \
                    beat["start"] + beat["duration"] - time.time()
                if duration > beat["duration"]:
                    duration = beat["duration"]
                # print(time.time() - start_time - beat["start"])
                # print(duration)
                if duration > 0:
                    light_pattern(lights, beat, start_time, duration,
                                  min_loudness, max_loudness, hue_shift, int(pattern))
                else:
                    print("skip")
        while(spotify.get_audio_features()[0]["id"] == track):
            if (spotify.get_playback_position() < time.time() - start_time - 5):
                break
            continue


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
