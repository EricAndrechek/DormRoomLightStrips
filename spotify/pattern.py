from time import time
import leds
import time
from cmath import sin, cos, phase, pi
import random


class Spotify_patterns:
    def __init__(self, lights, brightness=1, rgb=False, spotify=False, division="beat"):
        self.lights = lights
        self.pattern = brightness
        self.spotify = spotify
        self.division = division

        self.current_track = ""
        self.hue_shift = 0
        self.min_loudness = 0
        self.max_loudness = 0
        self.beats = []
        self.current_beat = None

        self.state = None

    def circular_average(self, inputs):
        sum = 0
        for x in inputs:
            sum = sum + complex(cos(2 * pi * x), sin(2 * pi * x))
        return phase(sum) / (2 * pi)

    def get_beats_info(self):
        analysis = self.spotify.get_audio_analysis()
        if self.division == "tatum":
            self.beats = analysis["tatums"]
        else:
            self.beats = analysis["beats"]
        segments = analysis["segments"]
        spot = 0
        loudness = 0
        pitch = 0
        spot_length = len(segments)
        for beat in self.beats:
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
                pitch = self.circular_average(pitches)
            beat["loudness"] = loudness
            beat["pitch"] = pitch

    def pattern1(self):
        loudness = (self.beat["loudness"] - self.min_loudness) / \
            (self.max_loudness - self.min_loudness)
        distance = int(loudness * 30)
        hsv = ((self.beat["pitch"] + self.hue_shift) % 1, 0.99, 0.99)
        self.lights.ceiling_region_fill(0, 3, hsv, "r")
        self.lights.ceiling_region_fill(0, 3, hsv, "l")
        self.lights.update()
        for i in range(3, distance):
            self.lights.ceiling_set_pixel(i, hsv, "r")
            self.lights.ceiling_set_pixel(i, hsv, "l")
            self.lights.update()
            time.sleep(self.duration / 8 / distance)
        for i in range(distance - 1, 2, -1):
            if self.duration < 0.2:
                self.lights.ceiling_region_fill(3, 84, (0, 0, 0))
                self.lights.update()
                break
            self.lights.ceiling_set_pixel(i, (0, 0, 0), "r")
            self.lights.ceiling_set_pixel(i, (0, 0, 0), "l")
            self.lights.update()
            time.sleep(self.duration / 3 / distance)

    def update_state2(self):
        for b in self.state:
            if (b[3] > 43):
                self.state.remove(b)
                continue
            self.lights.ceiling_set_pixel(b[3], (0, 0, 0), "r")
            self.lights.ceiling_set_pixel(b[3], (0, 0, 0), "l")
            b[3] = b[3] + 1
            if (b[3] + b[2] <= 43):
                self.lights.ceiling_set_pixel(b[3] + b[2], b[1], "r")
                self.lights.ceiling_set_pixel(b[3] + b[2], b[1], "l")

    def pattern2(self):
        if self.state == None:
            self.state = []

        loudness = (self.beat["loudness"] - self.min_loudness) / \
            (self.max_loudness - self.min_loudness)
        if loudness != self.max_loudness:
            loudness = loudness ** 2
        length = 1 + int(loudness * 7)
        hsv = ((self.beat["pitch"] + self.hue_shift) % 1, 0.99, 0.99)
        for i in range(0, length + 1):
            self.lights.ceiling_set_pixel(i, hsv, "r")
            self.lights.ceiling_set_pixel(i, hsv, "l")
            self.update_state2()
            self.lights.update()
            time.sleep(self.duration / 30)
        self.state.append([0, hsv, length, 0])
        for i in range(0, 5):
            self.update_state2()
            self.lights.update()
            time.sleep((i + 1) * self.duration / 30)

    def pattern3(self):
        if self.state == None:
            self.state = (0, (0, 0, 0))  # (center, hsv)

        hsv = ((self.beat["pitch"] + self.hue_shift) % 1, 0.99, 0.99)
        prev_start = self.state[0] - 10
        prev_end = self.state[0] + 10
        if self.beat["start"] == 0:
            center = random.randrange(0, 87)
        elif prev_start >= 0 and prev_end < 87:
            center = random.choice(
                list(range(0, prev_start + 1)) + list(range(prev_end, 87)))
        elif prev_end >= 87:
            center = random.randrange((prev_end) % 87, prev_start + 1)
        else:
            center = random.randrange(prev_end, prev_start % 87 + 1)
        self.lights.ceiling_set_pixel(center, hsv)
        self.lights.update()
        time.sleep(self.duration / 22)
        for i in range(1, 6):
            self.lights.ceiling_set_pixel(center + i, hsv)
            self.lights.ceiling_set_pixel(center - i, hsv)
            if self.beat["start"] != 0:
                self.lights.ceiling_set_pixel(self.state[0] - 6 + i, (0, 0, 0))
                self.lights.ceiling_set_pixel(self.state[0] + 6 - i, (0, 0, 0))
                self.lights.ceiling_region_fill(
                    self.state[0] - 5 + i, self.state[0] + 5 - i, (self.state[1][0], self.state[1][1], 1 - i * 0.2))
            self.lights.update()
            time.sleep(self.duration / 22)
        self.lights.ceiling_set_pixel(self.state[0], (0, 0, 0))
        self.lights.update()
        self.state = (center, hsv)

    def pattern4(self):
        if self.state == None:
            self.state = (0, 0, (0, 0, 0))  # (center, length, hsv)

        loudness = (self.beat["loudness"] - self.min_loudness) / \
            (self.max_loudness - self.min_loudness)
        if loudness != self.max_loudness:
            loudness = loudness ** 2
        hsv = ((self.beat["pitch"] + self.hue_shift) % 1, 0.99, 0.99)
        length = int(2 + 4 * loudness)
        if self.beat["start"] == 0:
            center = 0
        else:
            center = (self.state[0] + self.state[1] + length + 3) % 87

        if length >= self.state[1]:
            for i in range(0, length + 1):
                self.lights.ceiling_set_pixel(center + i, hsv)
                self.lights.ceiling_set_pixel(center - i, hsv)

                self.lights.ceiling_set_pixel(center + i + 43, hsv)
                self.lights.ceiling_set_pixel(center - i + 43, hsv)

                if self.beat["start"] != 0 and i < self.state[1]:
                    self.lights.ceiling_set_pixel(
                        self.state[0] - self.state[1] + i, (0, 0, 0))
                    self.lights.ceiling_set_pixel(
                        self.state[0] + self.state[1] - i, (0, 0, 0))
                    self.lights.ceiling_region_fill(
                        self.state[0] - self.state[1] + i + 1, self.state[0] + self.state[1] - i - 1, (self.state[2][0], self.state[2][1], 1 - ((i + 1) / self.state[1]) ** 2))
                    if i == self.state[1] - 1:
                        self.lights.ceiling_set_pixel(self.state[0], (0, 0, 0))

                    self.lights.ceiling_set_pixel(
                        self.state[0] - self.state[1] + i + 43, (0, 0, 0))
                    self.lights.ceiling_set_pixel(
                        self.state[0] + self.state[1] - i + 43, (0, 0, 0))
                    self.lights.ceiling_region_fill(
                        self.state[0] - self.state[1] + i + 1 + 43, self.state[0] + self.state[1] - i - 1 + 43, (self.state[2][0], self.state[2][1], 1 - ((i + 1) / self.state[1]) ** 2))
                    if i == self.state[1] - 1:
                        self.lights.ceiling_set_pixel(
                            self.state[0] + 43, (0, 0, 0))
                self.lights.update()
                time.sleep(self.duration / 14)

        if length < self.state[1]:
            for i in range(0, self.state[1]):
                if i < length + 1:
                    self.lights.ceiling_set_pixel(center + i, hsv)
                    self.lights.ceiling_set_pixel(center - i, hsv)

                    self.lights.ceiling_set_pixel(center + i + 43, hsv)
                    self.lights.ceiling_set_pixel(center - i + 43, hsv)
                if self.beat["start"] != 0:
                    self.lights.ceiling_set_pixel(
                        self.state[0] - self.state[1] + i, (0, 0, 0))
                    self.lights.ceiling_set_pixel(
                        self.state[0] + self.state[1] - i, (0, 0, 0))
                    self.lights.ceiling_region_fill(
                        self.state[0] - self.state[1] + i + 1, self.state[0] + self.state[1] - i - 1, (self.state[2][0], self.state[2][1], 1 - ((i + 1) / self.state[1]) ** 2))
                    if i == self.state[1] - 1:
                        self.lights.ceiling_set_pixel(self.state[0], (0, 0, 0))

                    self.lights.ceiling_set_pixel(
                        self.state[0] - self.state[1] + i + 43, (0, 0, 0))
                    self.lights.ceiling_set_pixel(
                        self.state[0] + self.state[1] - i + 43, (0, 0, 0))
                    self.lights.ceiling_region_fill(
                        self.state[0] - self.state[1] + i + 1 + 43, self.state[0] + self.state[1] - i - 1 + 43, (self.state[2][0], self.state[2][1], 1 - ((i + 1) / self.state[1]) ** 2))
                    if i == self.state[1] - 1:
                        self.lights.ceiling_set_pixel(
                            self.state[0] + 43, (0, 0, 0))
                self.lights.update()
                time.sleep(self.duration / 18)
        self.state = (center, length, hsv)

    def pattern5(self):
        hsv = ((self.current_beat["pitch"] + self.hue_shift) % 1, 0.99, 0.99)
        for i in range(0, 1):
            self.lights.ceiling_region_fill(0, 87, hsv)
            self.lights.update()
            time.sleep(self.duration / 80)
            self.lights.ceiling_region_fill(0, 87, (0, 0, 0))
            self.lights.update()
            time.sleep(self.duration / 5)

    def update_info(self):
        self.current_track = self.spotify.get_track_id()
        beats = self.get_beats_info()
        hues = []
        for beat in beats:
            if beat["loudness"] < self.min_loudness:
                self.min_loudness = beat["loudness"]
            if beat["loudness"] > self.max_loudness:
                self.max_loudness = beat["loudness"]
            hues.append(beat["pitch"])
        self.hue_shift = self.spotify.get_color(
        )[0] - self.circular_average(hues)

    def runner(self):
        if self.pattern == 0:
            self.pattern = 1
        self.lights.log.debug("spotify_lights_beat now running")
        while not self.lights.thread_kill:
            if self.spotify.is_playing():
                if self.current_track != self.spotify.get_track_id():
                    self.update_info()
                for self.current_beat in self.beats:
                    if not self.spotify.is_playing() or self.current_track != self.spotify.get_track_id():
                        break
                    start_time = time.time() - self.spotify.get_playback_position() - \
                        self.spotify.get_time_offset()
                    while time.time() < start_time + self.current_beat["start"]:
                        continue
                    if time.time() - start_time - self.current_beat["start"] > 0.3:
                        continue

                    self.duration = start_time + \
                        self.current_beat["start"] + \
                        self.current_beat["duration"] - time.time()
                    if self.duration > self.current_beat["duration"]:
                        self.duration = self.current_beat["duration"]

                    pattern_list = [self.pattern1, self.pattern2,
                                    self.pattern3, self.pattern4, self.pattern5]
                    pattern_list[self.pattern - 1]()
            else:
                time.sleep(250)
        self.lights.thread_end("spotify_lights_beat")
