#!/usr/bin/env bash

ts=$(date +%s%N)
mpiexec -n $1 python3 parallel-sieve.py $2 > /dev/null
val="$((($(date +%s%N) - $ts)/1000000))"
echo "$val"
