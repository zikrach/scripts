#
# /etc/bash.bashrc
#

export PYTHONSTARTUP=$HOME/.pythonrc
export EDITOR="/usr/bin/nano"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='\[\e[0;33m\]╔══\[\e[1;35m\] \t \[\e[0;33m\]══>\[\033[01;34m\] \w \n\e[0;33m╚═══> \[\033[01;32m\]\u\[\e[1;35m\]@\[\e[1;31m\]\H\[\033[01;34m\] \$\[\033[00m\] '
#PS1='[\u@\h \W]\$ '
PS2='> '
PS3='> '
PS4='+ '

case ${TERM} in
  xterm*|rxvt*|Eterm|aterm|kterm|gnome*)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033]0;%s@%s:%s\007" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
                                                        
    ;;
  screen)
    PROMPT_COMMAND=${PROMPT_COMMAND:+$PROMPT_COMMAND; }'printf "\033_%s@%s:%s\033\\" "${USER}" "${HOSTNAME%%.*}" "${PWD/#$HOME/~}"'
    ;;
esac

[ -r /usr/share/bash-completion/bash_completion   ] && . /usr/share/bash-completion/bash_completion

alias xterm="xterm -rv -fn 7x13 -fa /"PT Mono:size=10:antialias=true/""
alias upgrade="yaourt -Syua"
alias purge="yaourt -Rscn "

alias gs='git status '
alias ga='git add '
alias gb='git branch '
alias gc='git commit'
alias gd='git diff'
alias go='git checkout '
alias gk='gitk --all&'
#alias gx='gitx --all'

alias got='git '
alias get='git '

alias df='df -h'
alias g2m='wine /home/dima/.wine/drive_c/Program\ Files/MPlayer\ for\ Windows/MPlayer.exe'
alias mplayer='mplayer -vo vaapi:gl '
alias grep='grep --colour=auto'
alias torrent_start='sudo systemctl start rtorrent.path rtorrent.service nginx.service php-fpm.service'
alias torrent_stop='sudo systemctl stop rtorrent.path rtorrent.service nginx.service php-fpm.service'
alias startXP="xinit /usr/bin/VirtualBox --startvm \"xp\" --fullscreen -- /usr/bin/Xorg :1"
alias samba_start='sudo systemctl start smbd.service nmbd.service'
alias samba_stop='sudo systemctl stop smbd.service nmbd.service'
alias stop='sudo systemctl stop'
alias start='sudo systemctl start'
alias restart='sudo systemctl restart'
alias status='systemctl status'
alias debi_mount='ssh dimon@192.168.1.10 mount /var/www/wiki/ && ssh dimon@192.168.1.10 mount /media/katty_home/ && ssh dimon@192.168.1.10 mount /media/Download/'
alias analyze='systemd-analyze'
alias blame='systemd-analyze blame | head'

alias pylint="pylint --rcfile=~/.pylintrc"
alias pylint2="pylint2 --rcfile=~/.pylint2rc"
