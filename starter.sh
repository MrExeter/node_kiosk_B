#!/usr/bin/env bash

pid_return=($(lsof -i :5000));

echo "$pid_return"

if [ -z "$pid_return" ]
then
    # No flask process left running, all clear!
    echo All Clear!
else
    # Stray flask process still there, kill its pid
    echo We have something!
    echo "Killing PID : ${pid_return[10]}"
    kill "${pid_return[10]}"
fi

## Launch flask app
#echo "This script is about to run flask server"
#python run.py
#
## Launch "Display_script.sh"
#echo "This script is about to run display_status script."
#bash /home/pi/node_kiosk_B/app/utils/display_status.sh
