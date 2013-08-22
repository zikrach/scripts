#!/bin/bash
#@see	http://habrahabr.ru/blogs/shells/120502

# Клавиши для эмуляции я указывал кодом, потому что иногда утилита пропускает управляющую клавишу (Control) и выводит просто символ "c"
#
# sed производит замену символов. Команда y (sed "y/abcdef...) заменяет символ из первого шаблона
# на соответствующий ему символ из второго шаблона (sed «y/abcdefg.../фисвуап...; sed „y/abcdefg.../фисвуап...). 
#
# Строка дебага:	notify-send "DBG: $(xsel -b)"; exit 1;

emptystr="-----"
    # Запомним что было в буфере
buffer="$(xsel -b)"
selection="$(xsel)"

    # Получить выделенный текст #

    # переопределим буфер нашим значением, с которым будем сравнивать
echo -n "$emptystr" | xsel -b -i
    # без копирования мы может получить предыдущее выделение сохраненное в первичном буфере
xdotool key 37+54 #xdotool key Control+c

if [ "$(xsel -b)" == "$emptystr" ]; then #Текст не выделен
  xdotool key 37+50+113 #xdotool key Control+Shift+Left
  xdotool key 37+54 	#xdotool key Control+c
  selection="$(xsel -b)"
fi

    # Конвертируем выделенный текст иложим его в буфер обмена
echo -n "$selection" | sed "y/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.\/<>?@#\$^&\`~фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбюБЮ№ёЁ/фисвуапршолдьтщзйкыегмцчняФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯхъХЪжэЖЭбю.БЮ,\"№;:?ёЁabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ[]{};':\",.<>#\`~/" | xsel -b -i
result="$(xsel -b)"
#notify-send "DBG: $selection  ==>  $result"; exit 1;

    # Вставить содержимое буфера через триггер нажатия Ctrl + V
xdotool key 37+55 #xdotool key Control_L+v

#sleep 0 # вставка не успевает отработать, до возвращения в буфер первычных данных

    # Вернем в буфер то, что было в нем изначально
echo -n "$buffer" | xsel -b -i

    # Переключить раскладку клавиатуры
xdotool key 134 # xdotool Meta_R
