#!/usr/bin/env bash

echo standby 0 | cec-client -s -d 1

sleep 2s

echo sudo tvservice -o

sleep 4s

echo standby 0 | cec-client -s -d 1

echo sudo tvservice -o
