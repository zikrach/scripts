#!/bin/sh
CAST=$( xclip -o )
echo $CAST
if $CAST = "" ;
then exit 1;
fi
sp-sc sop://broker.sopcast.com:3912/$CAST 3908 8908 > /dev/null &
sleep 5
mplayer  http://localhost:8908/tv.asf
killall sp-sc
exit 0
