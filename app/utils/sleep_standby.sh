#!/usr/bin/env bash

echo standby 0 | cec-client -s -d 1

sleep 2s

echo tvservice -o

sleep 4s

echo standby 0 | cec-client -s -d 1

echo tvservice -o
