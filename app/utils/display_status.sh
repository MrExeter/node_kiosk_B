#!/usr/bin/env bash

while ( true )
do
    status=($(echo pow 0 | cec-client -s -d 1))

    if [ "${status[9]}" == "on" ]
    then
        echo "On" > '/home/pi/node_kiosk_B/app/utils/display_status.txt'
    elif [ "${status[9]}" == "standby" ]
    then
        echo "Standby" > '/home/pi/node_kiosk_B/app/utils/display_status.txt'
    else
        echo "ERROR" > '/home/pi/node_kiosk_B/app/utils/display_status.txt'
    fi

    sleep .10
done
