# Installs server configuration for ubuntu workers.


.PHONY: all run sync install

include env_vars
include includes/servers.mk
include includes/$(SERVER_TYPE).mk

all:
	@echo $(ENVVAR_NAME)
	$(error Please specify target. Valid targets are: install, run or sync)


sync:
	cd $(ROOT_DIR) && git pull origin master
	$(UPDATE_CMD)
	$(INSTALL_CMD) $(shell cat $(ROOT_DIR)/worker/system_dep.txt)
	cd $(ROOT_DIR) && pip install -r requirements.txt

run:
	python $(ROOT_DIR)/worker/deployer.py &	


install:
	$(MAKE) $(SERVER_TYPE)_install


startup:
	echo "cd $(ROOT_DIR);" >> start_amazon
	echo "make sync;" >> start_amazon
	echo "make run;" >> start_amazon
