#!/usr/bin/env bash
COUNTER=0;
UUIDS=($WORKERS_UUID);
NAMES=($WORKERS_NAME);
for d in ${WORKERS_DIR}; do 
	exec -a $d watchmedo shell-command \
	    --patterns="*.zip" \
	    --command='xe snapshot-revert snapshot-uuid=${UUIDS[COUNTER]};xe vm-start -u root vm=${NAMES[COUNTER]};scp ${watch_src_path} ${WORKER_USER}@${d}:${WORKER_MACHINE_DIR}/;rm -rf ${watch_src_path};' \
	    $d;
	let COUNTER=COUNTER+1;
done;
