#!/bin/sh
fdate="$*"
if [ ${#fdate} = 0 ]
then
   fdate=`date +%Y-%m-%d`
fi
#
cat /var/log/pacman.log | grep -e $fdate | grep -e 'installed \| upgraded' | awk -F' ' '{print $5, $6, $7, $8 }'

