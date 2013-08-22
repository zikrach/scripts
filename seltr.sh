#!/usr/bin/env bash
# http://habrahabr.ru/blogs/linux/137215/
text="$(xsel -o)"
translate="$(wget -U "Mozilla/5.0" -qO - "http://translate.google.com/translate_a/t?client=t&text=$(echo $text | sed "s/[\"'<>]//g")&sl=auto&tl=ru" | sed 's/\[\[\[\"//' | cut -d \" -f 1)"
echo "$translate" | xclip -selection clipboard # копировать перевод в буфер
notify-send -u critical "$text" "$translate" # вывести уведомление
