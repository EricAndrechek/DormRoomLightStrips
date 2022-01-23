#!/bin/bash

pid = $(nohup sudo python3 switches/color_rotate.py $1 $2 $3 $4)
echo $pid > process.txt