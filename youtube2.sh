#!/bin/sh
YOUTUBE=$( xclip -o )
if $YOUTUBE = "" ;
then exit 1;
fi
RESOLUTION="$(zenity --list --radiolist --title="Разрешение" --text "Укажите разрешение воспроизводимого файла" --column "" --column "Разрешение" FALSE "144" FALSE "180" FALSE "240" FALSE "340" FALSE "360" TRUE "480" FALSE "720" FALSE "1080" --height 450)"
youtube-viewer --resolution=$RESOLUTION --cache=90000 $YOUTUBE
exit 0
