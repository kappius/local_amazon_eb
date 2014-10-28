# Installs server configuration for centos supervisor'.

include env_vars
include includes/servers.mk
include includes/$(SERVER_TYPE).mk


.PHONY: all up run sync

all:
	$(error Please specify target. Valid targets are: install, run or sync)


sync:
	cd $(ROOT_DIR) && git pull origin master
	$(INSTALL_CMD) $(shell cat $(ROOT_DIR)/supervisor/system_dep.txt)
	cd $(ROOT_DIR) && pip install -r requirements.txt

run:
	bash $(ROOT_DIR)/supervisor/start.sh > $(ROOT_DIR)/supervisor/start.log &

install:
	$(MAKE) $(SERVER_TYPE)_install
	$(MAKE) user

startup:
	echo "cd $(ROOT_DIR);" >> start_amazon
	echo "make sync ON=supervisor;" >> start_amazon
	echo "make run ON=supervisor;" >> start_amazon
