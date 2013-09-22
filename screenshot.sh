#!/bin/bash

init()
{
    ACTIONS[0]="window/region,screen"
    ACTIONS[1]="drop,save"
    ACTIONS[2]="create random,ask,incremental pattern"
    ACTIONS[3]="screenshot-%05d.png"
    ACTIONS[4]="0,5,10,30,60"
    ACTIONS[5]="yes,no"
    ACTIONS[6]="no,yes"

    PROMPT[0]="Capture region"
    PROMPT[1]="Picture file"
    PROMPT[2]="File name"
    PROMPT[3]="File name pattern"
    PROMPT[4]="Delay"
    PROMPT[5]="Copy to clipboard"
    PROMPT[6]="Show links in a dialog"

    IND_CAPTURE_REGION=0
    IND_FILESAVE=1
    IND_FILENAME=2
    IND_PATTERN=3
    IND_DELAY=4
    IND_COPY_CLIPBOARD=5
    IND_SHOW_LINKS=6

    LOG="/var/log/screenshot.log"
#    FONT='Droid\ Sans\ Mono-9'
    FONT='-xos4-terminus-*-*-*-*-16-*-*-*-*-*-*-*'
    DMENU="dmenu -fn $FONT"
    IMAGEPASTE_CMD="imp"
    SCREENSHOT_CMD="scrot"
    SCREENSHOT_OPTIONS=
    OPTIONS=
    COUNT=${#ACTIONS[*]}
    BASEDIR="/home/`whoami`/pic/screenshot/scrot"
    CACHE="/tmp/screenshot.cache.sh"
    PATTERN_INDEX=0
}

load_cache()
{
    source $CACHE
}

save_cache()
{
    echo -n > $CACHE
    for (( i = 0; i < ${#OPTIONS[*]}; i++ ))
    do
        echo "OPTIONS[$i]=\"${OPTIONS[$i]}\"" >> $CACHE
    done
    echo "PATTERN_INDEX=\"$PATTERN_INDEX\"" >> $CACHE
}

random_filename()
{
    TMP=`mktemp --suffix=.scrot`
    BASE=`basename $TMP`
    FILENAME="$BASEDIR/$BASE.png"
}

ask_filename()
{
    FILENAME=`zenity --entry --text "Enter filename" --entry-text "$BASEDIR/"`
}

set_next_pattern_filename()
{
    FILENAME="$BASEDIR/$(printf ${OPTIONS[$IND_PATTERN]} $PATTERN_INDEX)"
    PATTERN_INDEX=$(($PATTERN_INDEX + 1))

    while [ -e "$FILENAME" ]; do
        FILENAME="$BASEDIR/$(printf ${OPTIONS[$IND_PATTERN]} $PATTERN_INDEX)"
        PATTERN_INDEX=$(($PATTERN_INDEX + 1))
    done
}

ask_options()
{
    for i in $(seq 0 $(($COUNT - 1)))
    do
        # if we are about to ask patern and
        # it wasn't the choise in prev question, continue
        if [ "$i" -eq "$IND_PATTERN" -a "${OPTIONS[$IND_FILENAME]}" != "incremental pattern" ]
        then
            continue
        fi

        OP=`echo ${ACTIONS[$i]} | tr "," "\n" | $DMENU -p "${PROMPT[$i]}"`

        if [ ! -n "$OP" ]; then
            exit 0
        fi

        OPTIONS[$i]=$OP
    done
}

parse_options()
{
    # parse options and ask user questions, if any
    ITEM=${OPTIONS[$IND_CAPTURE_REGION]}
    case "$ITEM" in
        window/region)
            SCREENSHOT_OPTIONS="-b -s"
            ;;
        screen)
            ;;
    esac

    ITEM=${OPTIONS[$IND_FILESAVE]}
    case "$ITEM" in
        save)
            # Dont touch BASEDIR
            ;;
        drop)
            BASEDIR="/tmp"
            ;;
    esac

    ITEM=${OPTIONS[$IND_FILENAME]}
    case "$ITEM" in
        ask)
            ask_filename
            ;;
        "create random")
            random_filename
            ;;
        "incremental pattern")
            set_next_pattern_filename
            ;;
    esac

    ITEM=${OPTIONS[$IND_DELAY]}
    SCREENSHOT_OPTIONS="$SCREENSHOT_OPTIONS -d $ITEM"
}

check_existence()
{
    if [ -e "$FILENAME" ]
    then
        zenity --question --text "File already exists. Overwrite?"
        OVERWRITE=$?
        if [ $OVERWRITE -ne 0 ]
        then
            exit 1
        fi
    fi
}

do_screenshot()
{
    rm -f "$FILENAME"
    mkdir -p `dirname "$FILENAME"`
    $SCREENSHOT_CMD $SCREENSHOT_OPTIONS "$FILENAME"
    CMD="$IMAGEPASTE_CMD $FILENAME"
    URL="`$CMD`"

    echo "$FILENAME -> $URL" >> $LOG
}

copy_to_clipboard()
{
    if [ ${OPTIONS[$IND_COPY_CLIPBOARD]} == "yes" ]
    then
        echo "$URL" | xclip -selection primary
        echo "$URL" | xclip -selection clipboard
    fi
}

show_links()
{
    if [ ${OPTIONS[$IND_SHOW_LINKS]} == "yes" ]
    then
        zenity --info --no-wrap --text "$FILENAME\n$URL"
    fi
}

init
if [ -e "$CACHE" -a "$1" == "cached" ]
then
    load_cache
else
    ask_options
fi
save_cache
parse_options
check_existence
do_screenshot
copy_to_clipboard
show_links

exit 0

