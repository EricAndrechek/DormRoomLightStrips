#!/usr/bin/env python3
import serial
import time

class connection:
    def __init__(self, port, baudrate):
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.reset_input_buffer()
        ser.write("comm".encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        if line == "good":
            print("Connected to Arduino!")
        else:
            print("Failed to connect: " + line)
        self.ser = ser
    def show(self):   
        self.ser.write("show".encode('utf-8'))
        line = self.ser.readline().decode('utf-8').rstrip()
        if line != "data":
            print("Failed to push update: " + line)
            self.ser.reset_input_buffer()
    def set_pixel(self, pixel, gbr):
        g, b, r = gbr
        char_map = self.get_char_map(pixel, g, b, r)
        self.ser.write("{}\n".format(char_map).encode('utf-8'))
        line = self.ser.readline().decode('utf-8').rstrip()
        if line != char_map:
            print("Failed to push data: " + line)
            self.ser.reset_input_buffer()
    def get_char_map(self, n, g, b, r):
        n = int(n)
        g = int(g)
        b = int(b)
        r = int(r)
        # 32 -> 117 inclusively
        x = 9*int(g/86) + 3*int(b/86) + int(r/86)
        if n >= 59:
            x = x*2
        g = g % 86
        b = b % 86
        r = r % 86
        n = n % 59
        return chr(n+32) + chr(g+32) + chr(b+32) + chr(r+32) + chr(x+32)
    
    
