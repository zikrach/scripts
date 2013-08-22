#!/bin/bash

wallp_dir=/home/dima/Documents/teames/DesktopBackground
reload_time="300"
wallpapers=();
while read ; do
    wallpapers += $REPLY
done << (ls "$wallp_dir")

while true; do
    count=${#wallpapers[@]}
    rand=$((RANDOM % count + 1))     
    pcmanfm --set-wallpaper="$wallp_dir"/"${wallpapers[$rand]}" --wallpaper-mode=stretch
    sleep "$reload_time"
done
EOF
