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
	bash $(ROOT_DIR)/supervisor/start.sh > $(ROOT_DIR)/supervisor/start.log &

install:
	$(MAKE) $(SERVER_TYPE)_install
	$(MAKE) user

xenserver_install:
	yum -y install openssh-server python python-devel
	python2.7 --version || $(MAKE) add_python
	-mkdir -p $(WORKERS_DIR)
	$(MAKE) chkconfig_startup

add_python:
	wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
	xz -d Python-2.7.6.tar.xz
	tar -xvf Python-2.7.6.tar
	cd Python-2.7.6 && ./configure --prefix=/usr/local
	cd Python-2.7.6 && make
	cd Python-2.7.6 && make altinstall
	rm -rf Python*
	curl -L https://bootstrap.pypa.io/get-pip.py | python2.7

user:
	-adduser $(ACCESS_USER)
	-groupadd $(ACCESS_GROUP)
	-useradd -g $(ACCESS_USER) $(ACCESS_GROUP)
	chown -R $(ACCESS_USER):$(ACCESS_GROUP) $(INSTALL_DIR) 

startup:
	echo "#!/usr/bin/env bash" > start_amazon
	echo "# chkconfig: 345 99 10" >> start_amazon
	echo "# description: start-amazon-supervisor" >> start_amazon
	echo "cd $(ROOT_DIR);" >> start_amazon
	echo "make sync ON=supervisor;" >> start_amazon
	echo "make run ON=supervisor;" >> start_amazon

chkconfig_startup:
	$(MAKE) startup
	cp start_amazon /etc/init.d/
	chmod +x /etc/init.d/start_amazon
	chkconfig --add start_amazon
	chkconfig start_amazon on
