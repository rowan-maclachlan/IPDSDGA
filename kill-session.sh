#!/bin/bash

for s in $(screen -ls | egrep -o 'cmpt394_\w+'); do
	screen -S $s -X quit
done
