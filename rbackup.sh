#!/bin/sh

sudo sh -c "
    rsync -av --delete-excluded --exclude-from=backup.lst / /media/Download/BackUp/arch;
    date > /media/Download/BackUp/arch/BACKUP
"
