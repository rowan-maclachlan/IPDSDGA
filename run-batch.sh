#!/bin/bash

max=$(nproc 2> /dev/null)
max=${max:-8}

for p in $@; do
    while [[ "$(screen -ls | grep cmpt394 | wc -l)" -gt "$max" ]]; do
        sleep 1
    done
    echo "Starting $(basename -s .json $p)"
    screen -dmS "cmpt394_$(basename -s .json $p)" bash -c "./run.sh $p"
done

