#!/usr/bin/env bash

#echo standby 0 | cec-client -s -d 1
echo standby 0 | cec-client -s -d 1
sleep 4.1666s
echo standby 0 | cec-client -s -d 1
tvservice -o
