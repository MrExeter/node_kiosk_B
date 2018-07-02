#!/usr/bin/env bash

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

# Playlist directory path is passed in
VIDEOPATH=$1

SERVICE="omxplayer"

# now for our infinite loop!
while true; do
        if ps ax | grep -v grep | grep $SERVICE > /dev/null
        then
        sleep 1;
else
        for entry in $VIDEOPATH
        do
                clear
                # -r for stretched over the entire screen
                omxplayer -r $entry > /dev/null
        done
fi
done