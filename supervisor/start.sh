#!/usr/bin/env bash
export COUNTER=0;
export UUIDS=($WORKERS_UUID);
export NAMES=($WORKERS_NAME);

for d in ${WORKERS_DIR}; do 
	export IP=${d##*/};
	watchmedo shell-command \
	    --patterns="*.zip" \
	    --command="xe snapshot-revert snapshot-uuid=${UUIDS[$COUNTER]};xe vm-start -u root vm=${NAMES[$COUNTER]};"'scp ${watch_src_path} '"${WORKER_USER}@${IP}:${WORKER_MACHINE_DIR}/;"'rm -rf ${watch_src_path};' \
	    --wait \
	    --drop \
	    $d;
	let COUNTER=COUNTER+1;
	export COUNTER;
done;
