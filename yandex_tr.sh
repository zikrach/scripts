#!/bin/bash
# Translate text with Yandex API
_zenity="/usr/bin/zenity"
_out="/tmp/translate.output.$$"

if [ "$(xclip -o)" ]
then
	text=$(xsel -o)
else
	text=$(${_zenity} --title  "Enter text" --entry)
fi

#text=$(${_zenity} --title  "Enter text" --entry --entry-text="$(xclip -o)" )
#text=$(xsel -o)

if [ $? -eq 0 ]
then
  wget -O ${_out} http://translate.yandex.ru/tr.json/translate --post-data="srv=tr-text&lang=en-uk&text=$text"
  sed -i 's/"//g' ${_out}
  ${_zenity} --timeout=3 --width=600 --height=240  \
         --title "Translation for $text" \
         --text-info --filename=${_out} 
  /bin/rm ${_out}
fi

