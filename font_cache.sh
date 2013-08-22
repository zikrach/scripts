#!/usr/bin/bash
echo "Старт Создание кэша иконок и шрифтов"
# обновление кэша иконок в своей папке
for d in ~/.icons/*; do gtk-update-icon-cache -f $d; done
# обновление кэша иконок в системе
for d in /usr/share/icons/*; do sudo gtk-update-icon-cache -f $d; done
# обновление кэша шрифтов
sudo fc-cache -fv
fc-cache ~/.fonts
echo "Окончание Создания кэша иконок и шрифтов"
