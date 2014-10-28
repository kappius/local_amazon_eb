include $(ROOT_DIR)/includes/startup.mk

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
