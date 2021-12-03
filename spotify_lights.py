from time import time
import leds
import time
from spotify import get_audio_analysis
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


def wave(lights, beat, start_time, min_loudness, max_loudness):
    print(beat)
    loudness = (beat["loudness"] - min_loudness) / \
        (max_loudness - min_loudness)
    distance = int(loudness * 44)
    duration = beat["duration"]
    hsv = (beat["pitch"], 0.99, 0.99)
    for i in range(0, distance):
        lights.ceiling_set_pixel(i, hsv, "r")
        lights.ceiling_set_pixel(i, hsv, "l")
        lights.update()
        time.sleep(duration / 10 / distance)
    for i in range(distance - 1, -1, -1):
        if time.time() > start_time + duration:
            print("fail")
            lights.ceiling_region_fill(0, 87, (0, 0, 0))
            lights.update()
            break
        lights.ceiling_set_pixel(i, (0, 0, 0), "r")
        lights.ceiling_set_pixel(i, (0, 0, 0), "l")
        lights.update()
        time.sleep(duration / 3 / distance)
    return duration


def main(lights):
    start_time = time.time()
    min_loudness = 0
    max_loudness = 0
    beats = get_beats_info()
    print(beats)
    for beat in beats:
        if beat["loudness"] < min_loudness:
            min_loudness = beat["loudness"]
        if beat["loudness"] > max_loudness:
            max_loudness = beat["loudness"]
    for beat in beats:
        wave(lights, beat, start_time, min_loudness, max_loudness)
        start_time = start_time + beat["duration"]


if __name__ == '__main__':
    lights = leds.light_strip()
    main(lights)
