from types import resolve_bases
import board
import neopixel
import colorsys
import time
import math


class light_strip:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            board.D18, 118, auto_write=False, pixel_order=neopixel.GRB)
        self.states = {
            # small sections:
            "tv_section": {
                "region": [0, 16],
                "ceiling": [0, 0],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "jayden_lamp": {
                "region": [16, 31],
                "ceiling:": [0, 0],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "window_section": {
                "region": [31, 49],
                "ceiling": [14, 32],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "jayden_bed": {
                "region": [49, 61],
                "ceiling": [32, 44],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "eric_bed": {
                "region": [61, 74],
                "ceiling": [44, 57],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "door_section": {
                "region": [74, 91],
                "ceiling": [57, 74],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "eric_desk": {
                "region": [91, 104],
                "ceiling": [74, 87],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "jayden_desk": {
                "region": [104, 118],
                "ceiling": [0, 14],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            # intermediate sections:
            "tv_wall": {
                "region": [91, 118],
                "ceiling": [-13, 14],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "bed_wall": {
                "region": [49, 74],
                "ceiling": [32, 57],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            # larger sections:
            "jayden_half": {
                "region": [104, 61],
                "ceiling": [0, 44],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            "eric_half": {
                "region": [61, 104],
                "ceiling": [44, 87],
                "state": 0,
                "hsv": (0, 0, 0.99)
            },
            # whole thing:
            "main": {
                "region": [31, 118],
                "ceiling": [0, 87],
                "state": 0,
                "hsv": (0, 0, 0.99)
            }
        }

    def correct_color(self, hsv):
        red = 0
        yellow = 0.04
        green = 1/3
        cyan = 0.5
        blue = 2/3
        magenta = 0.96

        hue = hsv[0] % 1
        if (hue < 1/6):
            hue = hue * 6 * (yellow - red) + red
        elif (hue >= 1/6 and hue < 1/3):
            hue = (hue - 1/6) * 6 * (green - yellow) + yellow
        elif (hue >= 1/3 and hue < 1/2):
            hue = (hue - 1/3) * 6 * (cyan - green) + green
        elif (hue >= 1/2 and hue < 2/3):
            hue = (hue - 1/2) * 6 * (blue - cyan) + cyan
        elif (hue >= 2/3 and hue < 5/6):
            hue = (hue - 2/3) * 6 * (magenta - blue) + blue
        else:
            hue = (hue - 5/6) * 6 * (1 - magenta) + magenta
        return (hue, hsv[1] ** 0.2, hsv[2])

    def hsv_to_gbr(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        grb = (256 * rgb[1], 256 * rgb[0], 256 * rgb[2])
        return grb

    def hex_to_hsv(self, hex):
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        hsv = colorsys.rgb_to_hsv(r/256, g/256, b/256)
        return hsv

    def hsv_to_hex(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        hex = ""
        for i in range(3):
            hex += hex(int(rgb[i] * 255))[2:].zfill(2)
        return hex

    def all_off(self):
        self.region_fill(0, 118, (0, 0, 0))

    def set_pixel(self, pixel, hsv, update="True"):
        self.pixels[pixel] = self.hsv_to_gbr(hsv)
        if (update):
            self.pixels.show()

    def fill_region_by_name(self, region, hsv):
        ceiling = self.states[region].ceiling
        self.states[region].hsv = hsv
        self.states[region].state = 1
        self.ceiling_region_fill(ceiling[0], ceiling[1], hsv)
    
    def region_off(self, region):
        self.states[region].state = 0
        self.ceiling_region_fill(self.states[region].ceiling[0], self.states[region].ceiling[1], (0, 0, 0))

    def region_fill(self, start, end, hsv, update=True):
        # not inclusive of end
        hsv = self.correct_color(hsv)
        if (start > end):
            return None
        if (end != 118):
            for i in range(start, end):
                try:
                    self.pixels[i] = (0, 0, 0)
                    self.pixels[i] = self.hsv_to_gbr(hsv)
                except IndexError:
                    print("Skipped pixel at index " + str(i))
        else:
            for i in range(start, 117):
                try:
                    self.pixels[i] = (0, 0, 0)
                    self.pixels[i] = self.hsv_to_gbr(hsv)
                except IndexError:
                    print("Skipped pixel at index " + str(i))
            self.set_pixel(117, hsv)
        if (update):
            self.pixels.show()

    def ceiling_region_fill(self, start, end, hsv, direction="r", update="True"):
        if (direction == "r"):
            if (end - start > 86):
                self.region_fill(31, 118, hsv, update)
                return start
            start = 104 + start % 87
            end = 104 + end % 87
            if (start > 117):
                start = start - 87
            if (end > 118):
                end = end - 87
            if (end >= start):
                self.region_fill(start, end, hsv, update)
            else:
                self.region_fill(start, 118, hsv, update)
                self.region_fill(31, end, hsv, update)
            return start
        if (direction == "l"):
            self.ceiling_region_fill(-end, -start, hsv, "r", update)
            start = 103 - start % 87
            if (start < 31):
                start = start + 87
            return start

    def status(self, region):
        return self.states[region].state

    def get_hex(self, region):
        return self.hsv_to_hex(self.states[region].hsv)

    def get_brightness(self, region):
        return self.states[region].hsv[2]

    def set_brightness(self, region, brightness):
        hsv = (self.states[region].hsv[0], self.states[region].hsv[1], brightness)
        self.fill_region_by_name(region, hsv)

    def region_color(self, region, color):
        hsv = self.hex_to_hsv(color)
        self.fill_region_by_name(region, hsv)
