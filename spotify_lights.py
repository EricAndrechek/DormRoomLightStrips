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

        if spot < spot_length:
            while segments[spot]["start"] < beat["start"] + beat["duration"]:
                loudnesses.append(segments[spot]["loudness_max"])
                for pitch in segments[spot]["pitches"]:
                    pitches.append(pitch)
                segments_count = 0
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


if __name__ == '__main__':
    print(get_beats_info())
