export INSTALL_CMD=yum install -y

# Create user anda configure folder permission 
user:
	-adduser $(ACCESS_USER)
	-groupadd $(ACCESS_GROUP)
	-useradd -g $(ACCESS_USER) $(ACCESS_GROUP)
	chown -R $(ACCESS_USER):$(ACCESS_GROUP) $(INSTALL_DIR) 

