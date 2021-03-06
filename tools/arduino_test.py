#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()

    successful = 0
    for i in range(0, 118):
        ser.write(b"comm\n")
        line = ser.readline().decode('utf-8').rstrip()
        if line == "good":
            successful += 1
        else:
            print("Failed: " + line)
    print("{}/118".format(successful))

    successful = 0
    for i in range(0, 118):
        ser.write(b"show\n")
        line = ser.readline().decode('utf-8').rstrip()
        if line == "data":
            successful += 1
        else:
            print("Failed: " + line)
    print("{}/118".format(successful))

    successful = 0
    for i in range(0, 118):
        data = chr(0) + chr(0) + chr(0) + chr(0)
        ser.write(data.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        if line == data:
            successful += 1
        else:
            print("Failed: " + line)
    print("{}/118".format(successful))