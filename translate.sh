#!/bin/bash

TEXT=$(xclip -o)
TRANSLATED_TEXT=$(/home/dima/bin/gctranslate.sh "$TEXT" en ru)
if [ ${#TEXT} -lt 120 ]; then
notify-send "$TRANSLATED_TEXT"
else
echo "$TRANSLATED_TEXT" | zenity --title="Перевод" --text-info
fi

