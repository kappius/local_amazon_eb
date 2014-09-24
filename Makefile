# Installs server configuration for ubuntu.

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


sync:
	cd $(INSTALL_DIR) && git pull origin master
	cd $(INSTALL_DIR) && apt-get install -y $(cat system_dep.txt)
	cd $(INSTALL_DIR) && pip install -r requirements.txt

run:
	python $(INSTALL_DIR)/deployer.py > $(INSTALL_DIR)/deployer.log &	

install:
	$(MAKE) ubuntu_install

ubuntu_install:
	apt-get update
	apt-get -y upgrade
	apt-get -y install openssh-server python python-dev apache2 libapache2-mod-wsgi libapache2-mod-proxy-html openssl python-pip
	-ln -s /etc/apache2/mods-available/proxy_http.load /etc/apache2/mods-enabled/proxy_http.load
	a2enmod ssl
	a2enmod proxy
	a2enmod proxy_http
	a2enmod wsgi
	-mkdir /etc/apache2/ssl
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/apache2/ssl/server.key -out /etc/apache2/ssl/server.crt
	-mkdir -p $(POOL_DIR)
	-mkdir -p $(TRASH_DIR)
	-mkdir -p $(DEPLOY_DIR)
	chown -R www-data:www-data $(INSTALL_DIR)
	-mkdir -p /private/var/log/apache2/
	cp python.conf /etc/apache2/sites-available/
	a2dissite 000-default
	a2ensite python
	service apache2 restart
	$(MAKE) startup

startup:
	echo "#!/usr/bin/env bash" > start_amazon
	echo "cd $(INSTALL_DIR);" >> start_amazon
	echo "make sync;" >> start_amazon
	echo "make run;" >> start_amazon
	$(MAKE) ubuntu_startup

ubuntu_startup:
	cp start_amazon /etc/init.d/
	chmod +x /etc/init.d/start_amazon
	update-rc.d start_amazon defaults
