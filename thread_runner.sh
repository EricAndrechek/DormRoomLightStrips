#!/bin/bash

sudo ./thread_killer.sh
sudo screen -S switch -dm bash -c "sudo python3 /home/pi/DormRoomLightStrips/switches/$1.py $2 $3 $4 $5"