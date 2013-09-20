#!/bin/bash
cmd="find -type f -print "
set_color_cmd="set_color"
if [ $2 ]; then cmd="$cmd -name \"$2\""; fi
color="green"
if [ $3 ]; then color=$3; fi

is_colored=1
hh=$(which "$set_color_cmd")
if [ $? -ne 0 ]; then is_colored=''; fi


$cmd | while read f; do
	cnt=$(grep -c "$1" "$f")
	if [ $cnt -gt 0 ]; then
		if [ $is_colored ]; then "$set_color_cmd" "$color"; fi
		echo "$f"
		if [ $is_colored ]; then "$set_color_cmd" normal; fi
		grep -n "$1" "$f"
	fi
done


