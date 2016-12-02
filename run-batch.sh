#!/bin/bash

for params in $@; do
    if tmux list-sessions | grep 'cmpt394'; then
        tmux new-window -t cmpt394 "./run.sh $params; read"
    else
        tmux new-session -s cmpt394 -d  "./run.sh $params; read"
    fi
    tmux rename-window -t cmpt394 "$(basename $params)"
done

tmux attach -t cmpt394
