#!/usr/bin/env python3
import serial
import time

def try_connection(ser):
    ser.write("comm\n".encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()
    if line == "good":
        print("Connected to Arduino!")
        return True
    else:
        print("Failed to connect: " + line)
        return try_connection(ser)

def get_char_map(n, g, b, r):
    n = int(n)
    g = int(g)
    b = int(b)
    r = int(r)
    # 32 -> 117 inclusively
    x = 9*int(g/86) + 3*int(b/86) + int(r/86)
    if n >= 59:
        x = x+27
    g = g % 86
    b = b % 86
    r = r % 86
    n = n % 59
    return chr(n+33) + chr(g+33) + chr(b+33) + chr(r+33) + chr(x+33)

def char_map_decode(char_map):
    n = ord(char_map[0]) - 33
    g = ord(char_map[1]) - 33
    b = ord(char_map[2]) - 33
    r = ord(char_map[3]) - 33
    x = ord(char_map[4]) - 33
    if (x >= 27):
        n += 59
    x = x % 27
    h = int(x / 9)
    x = x % 9
    i = int(x / 3)
    x = x % 3
    j = x
    g = g + 86 * h
    b = b + 86 * i
    r = r + 86 * j
    return n, g, b, r

def char_tester(n, g, b, r):
    char_map = get_char_map(n, g, b, r)
    print("char_map: " + char_map)
    n, g, b, r = char_map_decode(char_map)
    print("n: " + str(n))
    print("g: " + str(g))
    print("b: " + str(b))
    print("r: " + str(r))

class connection:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
        except serial.SerialException:
            ser = serial.Serial('/dev/ttyACM1', baudrate, timeout=1)
        ser.reset_input_buffer()
        try_connection(ser)
        self.ser = ser
    def show(self):   
        self.ser.write("show\n".encode('utf-8'))
        line = self.ser.readline().decode('utf-8').rstrip()
        if line != "data":
            print("Failed to push update: " + line)
            self.ser.reset_input_buffer()
    def set_pixel(self, pixel, gbr):
        g, b, r = gbr
        char_map = get_char_map(pixel, g, b, r)
        to_write = "{}\n".format(char_map).encode('utf-8')
        self.ser.write(to_write)
        line = self.ser.readline().decode('utf-8').rstrip()
        expected = "{}: {} {} {} {}".format(char_map, pixel, int(g), int(b), int(r))
        if line != expected:
            print("Failed to push data: {}, received: {}, expected: {}".format(char_map, line, expected))
            self.ser.reset_input_buffer()
    
    
