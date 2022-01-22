#!/bin/bash

screen -S lights -dm bash -c 'cd /home/pi/DormRoomLightStrips && sudo python3 receiver.py'