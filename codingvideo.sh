#!/bin/bash
in=$1
if [ ! -f $in ]; then echo No input parametr ; exit -1
fi
ffmpeg -i "$in" -vn -y in.wav
sox in.wav fast.wav tempo 1.6
name=`echo $in | awk -F . '{ print $1 }'`
ffmpeg -r 40 -i "$in" -i fast.wav -map 0:0 -map 1:0 -f mp4 -vcodec h264 -s 852x480 -r 25 -vb 500k -strict -2 -acodec aac -ab 128k -y "$name".mp4
rm in.wav fast.wav

