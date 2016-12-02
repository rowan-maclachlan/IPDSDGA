#!/bin/bash

sprunge() {
    curl -sF 'sprunge=<-' http://sprunge.us
}

TOKEN=$(cat .secret/token)
EMAIL=$(cat .secret/email)

mkdir -p out

params=${1:-params/default.json}
output="out/$(date -u +"%Y-%m-%dT%H:%M:%S")"

python3 Surface.py ${params} | tee ${output}.log

log_url=$(sprunge < ${output}.log)
json_url=$(sprunge < ${output}.json)

# Do not send notification if token and email are empty
[[ "${TOKEN}" == "" ]] && exit
[[ "${EMAIL}" == "" ]] && exit

python3 pushbullet-notify.py \
    -a $TOKEN \
    -e $EMAIL \
    -t "Simulation Done" \
       "log: $log_url json: $json_url"

