#!/usr/bin/env bash

ts=$(date +%s%N)
python3 sieve.py $1 > /dev/null
val="$((($(date +%s%N) - $ts)/1000000))"
echo "$val"
