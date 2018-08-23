#!/usr/bin/env bash
#
echo sudo tvservice -o

sleep 3

echo sudo tvservice -p

sleep 3s

echo sudo tvservice -p

sleep 4s

echo on 0 | cec-client -s -d 1


sleep 4s

echo on 0 | cec-client -s -d 1
