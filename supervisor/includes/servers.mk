include $(ROOT_DIR)/includes/startup.mk

# This configure supervisor machine by system type

############ Servers Builder ##########
# Configure xenserver like,
# install python 2.7 if not exist and add pip for install the requiriments
xenserver_install:
	yum -y install openssh-server python python-devel
	python2.7 --version || $(MAKE) add_python
	$(MAKE) add_pip
	-mkdir -p $(WORKERS_DIR)
	$(MAKE) chkconfig_startup

# Configure centOS 7x64
centOS_7x64_install:
	yum -y install openssh-server python python-devel
	python2.7 --version || $(MAKE) add_python
	$(MAKE) add_pip
	-mkdir -p $(WORKERS_DIR)
	$(MAKE) chkconfig_startup

############ Utils ################ 
# Install  2.7.6 python version
add_python:
	wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
	xz -d Python-2.7.6.tar.xz
	tar -xvf Python-2.7.6.tar
	cd Python-2.7.6 && ./configure --prefix=/usr/local
	cd Python-2.7.6 && make
	cd Python-2.7.6 && make altinstall
	rm -rf Python*

# Install pip
add_pip:
	curl -L https://bootstrap.pypa.io/get-pip.py | python2.7
