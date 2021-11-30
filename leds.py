from types import resolve_bases
import board
import neopixel
import colorsys
import time
import math


class light_strip:
    # Defined sections and color calibrations
    tv_section = [0, 15]
    tv_section_r_offset = 0
    tv_section_g_offset = 0
    tv_section_b_offset = 0

    jayden_lamp = [16, 30]
    jayden_lamp_r_offset = 0
    jayden_lamp_g_offset = 0
    jayden_lamp_b_offset = 0

    window_section = [31, 48]
    window_section_r_offset = 0
    window_section_g_offset = 0
    window_section_b_offset = 0

    jayden_bed = [49, 60]
    jayden_bed_r_offset = 0
    jayden_bed_g_offset = 0
    jayden_bed_b_offset = 0

    eric_bed = [61, 73]
    eric_bed_r_offset = 0
    eric_bed_g_offset = 0
    eric_bed_b_offset = 0

    door_section = [74, 90]
    door_section_r_offset = 0
    door_section_g_offset = 0
    door_section_b_offset = 0

    eric_desk = [91, 103]
    eric_desk_r_offset = 0
    eric_desk_g_offset = 0
    eric_desk_b_offset = 0

    jayden_desk = [104, 117]
    jayden_desk_r_offset = 0
    jayden_desk_g_offset = 0
    jayden_desk_b_offset = 0

    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            board.D18, 118, auto_write=False, pixel_order=neopixel.GRB)
        # States and colors:

        self.main_state = 0
        self.main_hsv = (2/3, 0, 1)

        self.jayden_lamp_state = 0
        self.jayden_lamp_hsv = (0, 0, 0)

        self.window_section_state = 0
        self.window_section_hsv = (0, 0, 0)

        self.jayden_bed_state = 0
        self.jayden_bed_hsv = (0, 0, 0)

        self.eric_bed_state = 0
        self.eric_bed_hsv = (0, 0, 0)

        self.door_section_state = 0
        self.door_section_hsv = (0, 0, 0)

        self.eric_desk_state = 0
        self.eric_desk_hsv = (0, 0, 0)

        self.jayden_desk_state = 0
        self.jayden_desk_hsv = (0, 0, 0)

    def correct_color(self, hsv):
        hsv = (hsv[0], hsv[1] ** 0.2, hsv[2])
        return hsv

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

    def set_pixel(self, pixel, hsv):
        self.pixels[pixel] = self.hsv_to_gbr(hsv)
        self.pixels.show()

    def all(self, hsv):
        self.region_fill(0, 118, hsv)

    def region_fill(self, start, end, hsv):
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
        self.pixels.show()

    def loop_region_fill(self, start, end, hsv, direction):
        if (direction == "r"):
            start = 104 + start % 87
            end = 104 + end % 87
            if (start > 117):
                start = start - 87
            if (end > 118):
                end = end - 87
            if (end >= start):
                self.region_fill(start, end, hsv)
            else:
                self.region_fill(start, 118, hsv)
                self.region_fill(31, end, hsv)
            return start
        if (direction == "l"):
            self.loop_region_fill(-end, -start, hsv, "r")
            start = 103 - start % 87
            if (start < 31):
                start = start + 87
            return start

    def status(self, region):
        return self.main_state

    def get_hex(self, region):
        return self.hsv_to_hex(self.main_hsv)

    def get_brightness(self, region):
        return self.main_hsv[2]

    def set_brightness(self, region, brightness):
        self.main_hsv = (self.main_hsv[0], self.main_hsv[1], brightness)
        self.region_fill(0, 118, self.main_hsv)

    def region_color(self, region, color):
        hsv = self.hex_to_hsv(color)
        self.region_fill(region[0], region[1], hsv)
