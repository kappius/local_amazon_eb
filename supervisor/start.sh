#!/usr/bin/env bash
export COUNTER=0;
export UUIDS=($WORKERS_UUID);
export NAMES=($WORKERS_NAME);

# Monitors all folders in WORKERS_DIR,
# Command call the script task, basics work, 
# Rebuild machine, ip by ip and send package for deploy

# patterns: conditional to running task
# command: shell like command if patterns match! 
# wait: wait task finish
# for more information git@github.com:gorakhargosh/watchdog.git

# COUNTER: is used to map list of NAMES and UUIDS

for d in ${WORKERS_DIR}; do 
	export IP=${d##*/};
	watchmedo shell-command \
	    --patterns="*.zip" \
	    --command="${ENV_BASH} source watchmedo/${SERVER_TYPE}.sh"\
	    --wait \
	    --drop \
	    $d &
	let COUNTER=COUNTER+1;
	export COUNTER;
	echo $d;
done;
