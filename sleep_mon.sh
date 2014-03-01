#!/bin/bash
if [ "`xset -q | grep Monitor | awk '{print $3}'`" == "On" ]; then
        xset -dpms && notify-send -t 3000 "dpms выключен"&
        else
        xset +dpms && notify-send -t 3000 "dpms включен" &
fi

