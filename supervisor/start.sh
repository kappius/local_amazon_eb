#!/usr/bin/env bash
for d in ${WORKERS_DIR}; do 
	watchmedo shell-command \
	    --patterns="*.zip" \
	    --command='scp ${watch_src_path} ${WORKER_USER}@${d}:${WORKER_MACHINE_DIR}/;rm -rf ${watch_src_path};' \
	    $d
done;
