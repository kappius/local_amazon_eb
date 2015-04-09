# AutoStart service, like cron
updaterc_startup:
	echo "#!/usr/bin/env bash" > start_amazon
	$(MAKE) startup
	cp start_amazon /etc/init.d/
	chmod +x /etc/init.d/start_amazon
	update-rc.d start_amazon defaults

chkconfig_startup:
	echo "#!/usr/bin/env bash" > start_amazon
	echo "# chkconfig: 345 99 10" >> start_amazon
	echo "# description: start-amazon-supervisor" >> start_amazon
	$(MAKE) startup
	cp start_amazon /etc/init.d/
	chmod +x /etc/init.d/start_amazon
	chkconfig --add start_amazon
	chkconfig start_amazon on
