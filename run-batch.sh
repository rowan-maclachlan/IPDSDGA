#!/bin/bash

for p in $@; do
    screen -dmS "cmpt394_$(basename -s .json $p)" bash -c "./run.sh $p"
done

