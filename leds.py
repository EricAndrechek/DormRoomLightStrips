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

        self.state = 0
        self.hex = "ffffff"
        self.rgb = (255, 255, 255)

        self.tv_section_state = 0
        self.tv_section_hex = "000000"

        self.jayden_lamp_state = 0
        self.jayden_lamp_hex = "000000"

        self.window_section_state = 0
        self.window_section_hex = "000000"

        self.jayden_bed_state = 0
        self.jayden_bed_hex = "000000"

        self.eric_bed_state = 0
        self.eric_bed_hex = "000000"

        self.door_section_state = 0
        self.door_section_hex = "000000"

        self.eric_desk_state = 0
        self.eric_desk_hex = "000000"

        self.jayden_desk_state = 0
        self.jayden_desk_hex = "000000"

    def correct_color(self, rgb):
        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        hsv = (hsv[0], hsv[1] ** 0.2, hsv[2])
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        return rgb

    def all_pixels(self, rgb):
        self.region_fill(0, 117, rgb)

    def off(self):
        self.all_pixels((0, 0, 0))

    def hex_to_rgb(self, hex):
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        return (g, r, b)

    def on(self):
        # self.off()
        self.all_pixels(self.rgb)

    def region_fill(self, start, end, rgb):
        rgb = self.correct_color(rgb)
        if (start > end):
            return None
        for i in range(start, end):
            try:
                self.pixels[i] = (0, 0, 0)
                self.pixels[i] = rgb
            except IndexError:
                print("Skipped pixel at index " + str(i))
        self.pixels[end] = rgb
        self.pixels.show()

    def loop_region_fill(self, start, end, rgb, direction):
        if (direction == "r"):
            start = 104 + start % 88
            end = 104 + end % 88
            if (start > 117):
                start = start - 87
            if (end > 117):
                end = end - 87
            if (end >= start):
                if (end < 117):
                    self.region_fill(start, end, rgb)
                if (end == 117):
                    self.region_fill(start, 116, rgb)
                    self.set_pixel(117, rgb)
            else:
                self.region_fill(start, 116, rgb)
                self.set_pixel(117, rgb)
                self.region_fill(31, end, rgb)
            return start
        if (direction == "l"):
            self.loop_region_fill(end - 1, start - 1, rgb, "r")

    def status(self):
        return self.state

    def set_hex(self, hex):
        self.hex = hex
        time.sleep(0.1)
        self.rgb = self.hex_to_rgb(hex)
        time.sleep(0.1)
        self.on()

    def get_hex(self):
        return self.hex

    def set_pixel(self, pixel, rgb):
        self.pixels[pixel] = rgb
        self.pixels.show()
