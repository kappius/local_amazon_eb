 #!/usr/bin/env bash

# Need description
if [ -f ${watch_src_path} ];
	then 
	 # Rebuild DROPLET
	 # try to connect
	scp -o ConnectionAttempts=10000 ${watch_src_path} ${WORKER_USER}@${IP}:${WORKER_MACHINE_DIR}; fi 