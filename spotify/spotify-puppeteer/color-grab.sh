#!/bin/bash

xvfb-run -a --server-args="-screen 0 1280x800x24 -ac -nolisten tcp -dpi 96 +extension RANDR" node /home/eric/spotify-color-grab/get_color.js
