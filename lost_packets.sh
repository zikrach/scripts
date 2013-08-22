#!/bin/bash
#  https://wiki.archlinux.org/index.php/Pacman_%28Русский%29
#  Получение списка пакетов, которых нет в репозитории. v2
#  запускать от root
LANG=C; pacman -S `pacman -Qq` &>./pkg_install.txt
cat ./pkg_install.txt | grep error: > pkg_non_rep.txt
