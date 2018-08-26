#!/usr/bin/env bash

tvservice -p

sleep 2s
echo on 0 | cec-client -s -d 1

sleep 4s
echo on 0 | cec-client -s -d 1
