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
            print("Failed to connect to Arduino!")
        self.ser = ser
    def show(self):   
        self.ser.write("show".encode('utf-8'))
        line = self.ser.readline().decode('utf-8').rstrip()
        if line != "data":
            print("Failed to push data to Arduino! - Message from Arduino: " + line)
            self.ser.reset_input_buffer()
    def set_pixel(self, pixel, gbr):
        g, b, r = gbr
        g = chr(g)
        b = chr(b)
        r = chr(r)
        n = chr(pixel)
        self.ser.write("{}{}{}{}".format(n, g, b, r).encode('utf-8'))
    
    
