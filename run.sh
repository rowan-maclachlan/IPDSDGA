#!/bin/bash

haste() {
    a=$(cat);
    curl -X POST -s -d "${a}" 'http://hastebin.com/documents' | awk -F '"' '{print "http://hastebin.com/"$4}';
}

sprunge() {
    curl -sF 'sprunge=<-' http://sprunge.us
}

TOKEN=$(cat .secret/token 2> /dev/null)
EMAIL=$(cat .secret/email 2> /dev/null)

params_file=${1:-params/default.json}
params=$(basename -s .json ${params_file})
out="out/${params}_$(date +"%Y-%m-%d_%H.%M.%S")/"

mkdir -p ${out}
cd ${out}
python3 ../../Surface.py ../../${params_file} | tee run.log
cd -

# Do not send notification if token and email are empty
[[ "${TOKEN}" == "" ]] && exit
[[ "${EMAIL}" == "" ]] && exit

log_url=$(haste < ${out}/run.log)
json_url=$(haste < ${out}/data.json)

python3 pushbullet-notify.py \
    -a $TOKEN \
    -e $EMAIL \
    -t "Simulation Done: ${params}" \
       "log: ${log_url} json: ${json_url}" 


