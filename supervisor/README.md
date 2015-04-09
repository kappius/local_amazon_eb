# Supervisor

## Configure enviroment variables

look inside env_vars file and you see something like this

* export SERVER_TYPE=
* export WORKERS_DIR=
* export WORKERS_UUID=
* export WORKERS_NAME=
* export WORKER_USER=root
* export WORKER_MACHINE_DIR=/opt/deployer/pool
* export ACCESS_USER=deploy
* export ACCESS_GROUP=deploy

Read description and configure all after start supervisor

### SERVER_TYPE

actually we support
* xenserver
* centOS_7x64
You can make anothers configurations in /include/servers.mk

### WORKERS_DIR
 wherer has enviroment configuration files

### WORKERS_UUID
 the universally unique identifier

### WORKERS_NAME
<Need Description>

### WORKER_USER
 <Need Description>

### WORKER_MACHINE_DIR
where supervisor will running

### ACCESS_USER
User to deploy


### ACCESS_GROUP
group of user to deploy
