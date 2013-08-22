#!/usr/bin/bash
notify-send -u critical "$(xsel -o)" "$(python2 /home/dima/bin/tran.py "$(xsel -o | sed "s/[\"'<>]//g")")"

