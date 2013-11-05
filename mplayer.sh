#!/usr/bin/bash
xclip -o | sed -n 1p | xargs mplayer -cache 8192
