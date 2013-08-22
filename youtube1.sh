#!/bin/sh
YOUTUBE=$( xclip -o )
if $YOUTUBE = "" ;
then exit 1;
fi
youtube-viewer --resolution=480 --cache=90000 $YOUTUBE
exit 0
