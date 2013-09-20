#!/bin/bash
# @author	Allen Choong Chieng Hoon
# @date		2013-08-27
# @version	1.0
# Clean the old version files in yaourt

if [[ -a "$HOME/.yaourtrc" ]] ; then
	source "$HOME/.yaourtrc"
	if [ -d "$EXPORTDIR" ] ; then
		cd "$EXPORTDIR"
	else
		echo "No yaourt export directory. No action done."
		exit
	fi
else
	echo ".yaourtrc not found. No action done."
	exit
fi

read -p "Confirm clean old version files in \"$EXPORTDIR\" [y,n] " confirm
if [ "x$confirm" != xy ] ; then
	exit
fi

files=(`ls -r`)
for ((i=1;i<${#files[@]};i++)); do
	prev=`echo ${files[$i-1]} | sed 's@[0-9]\{1,\}@N@g'`
	curr=`echo ${files[$i]} | sed 's@[0-9]\{1,\}@N@g'`
	if [[ "$prev" == "$curr" ]] ; then
		echo "Delete ${files[$i]}"
		rm "${files[$i]}"
	fi
done
echo "Completed."
