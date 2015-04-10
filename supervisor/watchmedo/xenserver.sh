 #!/usr/bin/env bash

# Revert snapshot by UUID
# Start VM
# Send package to Worker
if [ -f ${watch_src_path} ];
	then xe snapshot-revert snapshot-uuid=${UUIDS[$COUNTER]};
	xe vm-start -u root vm=${NAMES[$COUNTER]};
	scp -o ConnectionAttempts=10000 ${watch_src_path} ${WORKER_USER}@${IP}:${WORKER_MACHINE_DIR}; fi 