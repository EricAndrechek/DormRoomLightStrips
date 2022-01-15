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

class connection:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
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
        char_map = self.get_char_map(pixel, g, b, r)
        to_write = "{}\n".format(char_map).encode('utf-8')
        self.ser.write(to_write)
        line = self.ser.readline().decode('utf-8').rstrip()
        if line != char_map:
            print("Failed to push data: {}, received: {}".format(to_write, line))
            self.ser.reset_input_buffer()
    def get_char_map(self, n, g, b, r):
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
    
    
