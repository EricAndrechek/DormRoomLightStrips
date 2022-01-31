from types import resolve_bases
import board
import neopixel
import colorsys
import requests
import json
import sys
sys.path.append("switches")
from switches import *
import os
import threading
import time
import logging


class light_strip:
    def __init__(self, is_receiver=False, is_transmitter=False, server=None):
        self.log = logging.getLogger("lights")
        self.log.setLevel(logging.DEBUG)
        self.log.basicConfig(format='[%(asctime)s] [%(levelname)s]: %(message)s', datefmt='%d/%b/%y %H:%M:%S')
        if is_receiver:
            self.pixels = neopixel.NeoPixel(
            board.D18, 118, auto_write=False, pixel_order=neopixel.GRB)
        self.homebridge_url = "http://192.168.2.16:8001/"
        self.receiver_url = "http://192.168.2.97:8000/"
        self.is_receiver = is_receiver
        self.is_transmitter = is_transmitter
        self.thread = None
        self.thread_kill = False
        self.states = {
            # small sections:
            "tv_section": {
                "region": [0, 16],
                "ceiling": [0, 0],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": []
            },
            "jayden_lamp": {
                "region": [16, 31],
                "ceiling:": [0, 0],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": []
            },
            "window_section": {
                "region": [31, 49],
                "ceiling": [14, 32],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "jayden_half"]
            },
            "jayden_bed": {
                "region": [49, 61],
                "ceiling": [32, 44],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "jayden_half", "bed_wall"]
            },
            "eric_bed": {
                "region": [61, 74],
                "ceiling": [44, 57],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "eric_half", "bed_wall"]
            },
            "door_section": {
                "region": [74, 90],
                "ceiling": [57, 73],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "eric_half"]
            },
            "eric_desk": {
                "region": [90, 104],
                "ceiling": [73, 87],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "eric_half", "tv_wall"]
            },
            "jayden_desk": {
                "region": [104, 118],
                "ceiling": [0, 14],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": [],
                "included_in": ["main", "jayden_half", "tv_wall"]
            },
            # intermediate sections:
            "tv_wall": {
                "region": [91, 118],
                "ceiling": [-13, 14],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": ["eric_desk", "jayden_desk", "jayden_half", "eric_half"],
                "included_in": ["main", "jayden_half", "eric_half"]
            },
            "bed_wall": {
                "region": [49, 74],
                "ceiling": [32, 57],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": ["eric_bed", "jayden_bed", "jayden_half", "eric_half"],
                "included_in": ["main", "jayden_half", "eric_half"]
            },
            # larger sections:
            "jayden_half": {
                "region": [104, 61],
                "ceiling": [0, 44],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": ["jayden_bed", "jayden_desk", "window_section", "bed_wall", "tv_wall"],
                "included_in": ["main", "bed_wall", "tv_wall"]
            },
            "eric_half": {
                "region": [61, 104],
                "ceiling": [44, 87],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": ["eric_bed", "eric_desk", "door_section", "bed_wall", "tv_wall"],
                "included_in": ["main", "bed_wall", "tv_wall"]
            },
            # whole thing:
            "main": {
                "region": [31, 118],
                "ceiling": [0, 87],
                "state": 0,
                "hsv": (0, 0, 0.99),
                "includes": ["window_section", "jayden_bed", "eric_bed", "door_section", "eric_desk", "jayden_desk", "tv_wall", "bed_wall", "jayden_half", "eric_half"],
                "included_in": []
            }
        }
        # get all switches from switches.json
        if server is not None:
            with open("switches.json") as f:
                self.switches = json.load(f)
            for switch in self.switches:
                self.states[switch["internal_name"]] = {}
                self.states[switch["internal_name"]]["state"] = 0
                if switch["is_rgb"]:
                    self.states[switch["internal_name"]]["hsv"] = (0, 0, 0.99)
                if switch["is_brightness_slider"]:
                    self.states[switch["internal_name"]]["brightness"] = 0
                    self.states[switch["internal_name"]]["brightness_max"] = switch["brightness_slider_max"]
        
            self.immune = [server, os.getpid()]
            # if it is a server, we should start the spotify thread in the background too
            self.log.debug("server initialized with pid {}".format(os.getpid()))

    def correct_color(self, hsv):
        red = 0
        yellow = 0.04
        green = 1 / 3
        cyan = 0.5
        blue = 2 / 3
        magenta = 0.96

        hue = hsv[0] % 1
        if (hue < 1 / 6):
            hue = hue * 6 * (yellow - red) + red
        elif (hue >= 1 / 6 and hue < 1 / 3):
            hue = (hue - 1 / 6) * 6 * (green - yellow) + yellow
        elif (hue >= 1 / 3 and hue < 1 / 2):
            hue = (hue - 1 / 3) * 6 * (cyan - green) + green
        elif (hue >= 1 / 2 and hue < 2 / 3):
            hue = (hue - 1 / 2) * 6 * (blue - cyan) + cyan
        elif (hue >= 2 / 3 and hue < 5 / 6):
            hue = (hue - 2 / 3) * 6 * (magenta - blue) + blue
        else:
            hue = (hue - 5 / 6) * 6 * (1 - magenta) + magenta
        return (hue, hsv[1] ** 0.2, hsv[2])

    def hsv_to_gbr(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        grb = (256 * rgb[1], 256 * rgb[0], 256 * rgb[2])
        return grb

    def hex_to_hsv(self, hex):
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        hsv = colorsys.rgb_to_hsv(r / 256, g / 256, b / 256)
        return hsv

    def hsv_to_hex(self, hsv):
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        r = int(rgb[0] * 256)
        g = int(rgb[1] * 256)
        b = int(rgb[2] * 256)
        return '%02x%02x%02x' % (r, g, b)

    def rgb_to_hsv(self, rgb):
        hsv = colorsys.rgb_to_hsv(rgb[0] / 256, rgb[1] / 256, rgb[2] / 256)
        return hsv

    def update(self):
        if self.is_receiver:
            self.pixels.show()
        else:
            requests.get(self.receiver_url + "update")

    def homebridge_push(self, region, status):
        requests.post(self.homebridge_url + region, json={
            "characteristic": "On",
            "value": status,
            "accessory": "HttpPushRgb",
            "service": "Light"
        })

    def all_off(self):
        self.kill_thread()
        for region in self.states:
            if self.states[region]["state"] == 1:
                if "includes" in self.states[region]:
                    self.region_off(region)
                else:
                    # alteranative to region_off for switches
                    self.states[region]["state"] = 0
                    self.homebridge_push(region, False)
        self.region_fill(0, 118, (0, 0, 0))
        self.update()

    def set_pixel(self, pixel, color, gbr=True):
        if gbr is False:
            color = self.hsv_to_gbr(self.correct_color(color))
        if self.is_receiver:
            self.pixels[pixel] = color
        else:
            requests.get("{}pixel/{}/{}/{}/{}".format(self.receiver_url, pixel, color[0], color[1], color[2]))

    def ceiling_set_pixel(self, pixel, hsv, direction="r"):
        if (direction == "r"):
            pixel = 104 + pixel % 87
            if (pixel > 117):
                pixel = pixel - 87
            self.set_pixel(pixel, hsv, gbr=False)
        if (direction == "l"):
            self.ceiling_set_pixel(-pixel - 1, hsv, "r")

    def fill_region_by_name(self, region, hsv):
        for included in self.states[region]["includes"]:
            if self.states[included]["state"] == 1:
                self.region_off(included)
                self.states[included]["state"] = 0
                # push update to homebridge here
                self.homebridge_push(included, False)
        for included in self.states[region]["included_in"]:
            if self.states[included]["state"] == 1:
                self.region_off(included)
                self.states[included]["state"] = 0
                # push update to homebridge here
                self.homebridge_push(included, False)
        self.kill_thread()
        ceiling = []
        try:
            ceiling = self.states[region]["ceiling"]
        except KeyError:
            ceiling = [0, 0]
        if (ceiling[0] == 0) and (ceiling[1] == 0):
            self.region_fill(
                self.states[region]["region"][0], self.states[region]["region"][1], hsv)
        else:
            self.ceiling_region_fill(ceiling[0], ceiling[1], hsv)
        self.states[region]["hsv"] = hsv
        self.states[region]["state"] = 1
        # push update to homebridge here
        self.homebridge_push(region, True)

    def region_off(self, region):
        self.states[region]["state"] = 0
        # push update to homebridge here
        self.homebridge_push(region, False)
        ceiling = []
        try:
            ceiling = self.states[region]["ceiling"]
        except KeyError:
            ceiling = [0, 0]
        if (ceiling[0] == 0) and (ceiling[1] == 0):
            self.region_fill(
                self.states[region]["region"][0], self.states[region]["region"][1], (0, 0, 0))
        else:
            self.ceiling_region_fill(
                self.states[region]["ceiling"][0], self.states[region]["ceiling"][1], (0, 0, 0))

    def region_fill(self, start, end, hsv):
        # not inclusive of end
        hsv = self.correct_color(hsv)
        if (start > end):
            return None
        if (end != 118):
            for i in range(start, end):
                try:
                    self.set_pixel(i, (0, 0, 0))
                    self.set_pixel(i, self.hsv_to_gbr(hsv))
                except IndexError:
                    self.log.warn("Index Error: Skipped pixel at index " + str(i))
                except TypeError:
                    self.log.warn("Type Error: Skipped pixel at index " + str(i))
        else:
            for i in range(start, 117):
                try:
                    self.set_pixel(i, (0, 0, 0))
                    self.set_pixel(i, self.hsv_to_gbr(hsv))
                except IndexError:
                    self.log.warn("Index Error: Skipped pixel at index " + str(i))
                except TypeError:
                    self.log.warn("Type Error: Skipped pixel at index " + str(i))
            self.set_pixel(117, self.hsv_to_gbr(hsv))

    def ceiling_region_fill(self, start, end, hsv, direction="r"):
        if (direction == "r"):
            if (end - start > 86):
                self.region_fill(31, 118, hsv)
                return start
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
            self.ceiling_region_fill(-end, -start, hsv, "r")
            start = 103 - start % 87
            if (start < 31):
                start = start + 87
            return start

    def smooth_transition(self, start, end, old_hsv, new_hsv, transition_time):
        # start and end for ceiling, time in s
        old_rgb = colorsys.hsv_to_rgb(old_hsv[0], old_hsv[1], old_hsv[2])
        new_rgb = colorsys.hsv_to_rgb(new_hsv[0], new_hsv[1], new_hsv[2])

        r_step = (new_rgb[0] - old_rgb[0]) / transition_time / 1000
        g_step = (new_rgb[1] - old_rgb[1]) / transition_time / 1000
        b_step = (new_rgb[2] - old_rgb[2]) / transition_time / 1000

        rgb = old_rgb
        for i in range(0, int(transition_time * 1000)):
            rgb = (rgb[0] + r_step, rgb[1] + g_step, rgb[2] + b_step)
            hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
            self.ceiling_region_fill(start, end, hsv)
            self.update()

    def status(self, region):
        return self.states[region]["state"]

    def get_hex(self, region):
        return str(self.hsv_to_hex(self.states[region]["hsv"]))

    def get_brightness(self, region):
        return int(self.states[region]["hsv"][2] * 100)

    def set_brightness(self, region, brightness):
        brightness = int(brightness)
        brightness = brightness / 100
        if (brightness == 1):
            brightness = 0.99
        hsv = (self.states[region]["hsv"][0],
               self.states[region]["hsv"][1], brightness)
        self.fill_region_by_name(region, hsv)

    def region_color(self, region, color):
        hsv = self.hex_to_hsv(color)
        self.fill_region_by_name(region, hsv)

    def region_on(self, region):
        self.fill_region_by_name(region, self.states[region]["hsv"])

    def get_all_states(self):
        return self.states

    def get_region_dict(self, region):
        return self.states[region]

    def switch_on(self, switch, brightness=None, color=None):
        self.all_off()
        if color is not None or "hsv" in self.states[switch]:
            if color is not None:
                color = self.hex_to_hsv(color)
            else:
                color = self.states[switch]["hsv"]
            self.states[switch]["hsv"] = color
        else:
            color = (0, 0, 0)
        if brightness is not None or "brightness" in self.states[switch]:
            if brightness is None:
                brightness = self.states[switch]["brightness"]
            brightness = int(brightness)
            self.states[switch]["brightness"] = brightness
        else:
            brightness = 100
        self.states[switch]["state"] = 1
        self.run_thread(switch, brightness, color)
        return 'on/set'
    def switch_off(self, switch):
        # stop thread process running switch_on
        self.all_off()
        self.states[switch]["state"] = 0
    
    def switch_brightness(self, region):
        return self.states[region]["brightness"]

    def run_thread(self, switch, brightness, color):
        targ = switch + ".main"
        self.kill_thread()
        self.thread = threading.Thread(target=eval(targ), args=(self, brightness, color), daemon=True)
        self.thread.start()

    def kill_thread(self):
        self.thread_kill = True
        while self.thread is not None and self.thread.is_alive():
            time.sleep(0.1)
        self.thread_kill = False
    
    def thread_end(self, name):
        self.states[name]["state"] = 0
        self.homebridge_push(name, False)
        self.log.debug(name + " has stopped")
        self.thread = None


