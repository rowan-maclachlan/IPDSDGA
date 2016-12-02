#!/bin/bash

sprunge() {
    curl -sF 'sprunge=<-' http://sprunge.us
}

TOKEN=$(cat .secret/token)
EMAIL=$(cat .secret/email)

mkdir -p out

params_file=${1:-params/default.json}
params=$(basename -s .json ${params_file})
output="out/${params}_$(date +"%Y-%m-%d_%H:%M:%S")"

python3 Surface.py ${params_file} | tee ${output}.log

log_url=$(sprunge < ${output}.log)
json_url=$(sprunge < ${output}.json)

# Do not send notification if token and email are empty
[[ "${TOKEN}" == "" ]] && exit
[[ "${EMAIL}" == "" ]] && exit

python3 pushbullet-notify.py \
    -a $TOKEN \
    -e $EMAIL \
    -t "Simulation Done: ${params}" \
       "log: $log_url json: $json_url"

