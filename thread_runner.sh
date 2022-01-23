#!/bin/bash

sudo screen -S switch -d -m bash -c "sudo python3 /home/pi/DormRoomLightStrips/switches/color_rotate.py $1 $2 $3 $4"