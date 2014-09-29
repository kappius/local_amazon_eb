# Installs server configuration for centos supervisor'.

include env_vars

.PHONY: all up run sync

all:
	$(error Please specify target. Valid targets are: install, run or sync)


sync:
	cd $(ROOT_DIR) && git pull origin master
	yum install -y $(shell cat $(ROOT_DIR)/supervisor/system_dep.txt)
	cd $(ROOT_DIR) && pip install -r requirements.txt

run:
	bash $(ROOT_DIR)/supervisor/start.sh

install:
	$(MAKE) centos_install

centos_install:
	yum -y install openssh-server python python-dev python-pip
	-mkdir -p $(WORKERS_DIR)
	$(MAKE) startup

startup:
	echo "#!/usr/bin/env bash" > start_amazon
	echo "# chkconfig: 345 99 10" >> start_amazon
	echo "# description: start-amazon-supervidor" >> start_amazon
	echo "cd $(ROOT_DIR);" >> start_amazon
	echo "make sync ON=supervisor;" >> start_amazon
	echo "make run ON=supervisor;" >> start_amazon
	$(MAKE) centos_startup

centos_startup:
	cp start_amazon /etc/init.d/
	chmod +x /etc/init.d/start_amazon
	chkconfig --add start_amazon
	chkconfig start_amazon on
