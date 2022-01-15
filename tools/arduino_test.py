#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    successful = 0
    for i in range(0, 118):
        ser.write(b"comm\n")
        line = ser.readline().decode('utf-8').rstrip()
        if line == "good":
            successful += 1
        else:
            print("Failed: " + ord(line))
    print("" + successful + "/118")