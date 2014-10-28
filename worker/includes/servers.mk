include $(ROOT_DIR)/includes/startup.mk

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
	$(MAKE) updaterc_startup
