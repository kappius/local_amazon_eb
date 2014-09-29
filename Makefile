# Installs server configuration for ubuntu workers and centos supervisor.

INSTALL_DIR = $(abspath /opt/deployer)
export INSTALL_DIR
POOL_DIR = $(abspath /opt/deployer/pool)
export POOL_DIR
TRASH_DIR = $(abspath /opt/deployer/trash)
export TRASH_DIR
DEPLOY_DIR = $(abspath /opt/deployer/deploy)
export DEPLOY_DIR


.PHONY: all install sync run

all:
	$(error Please specify target. Valid targets are: install, run or sync)


install startup run sync:
ifeq ($(ON),supervisor)
	$(MAKE) install -C supervisor
else
	$(MAKE) install -C worker
endif
