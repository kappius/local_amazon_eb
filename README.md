# INSTALL
```
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install openssh-server python python-dev apache2 libapache2-mod-wsgi libapache2-mod-proxy-htmlgit
sudo ln -s /etc/apache2/mods-available/proxy_http.load /etc/apache2/mods-enabled/proxy_http.load
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod wsgi
sudo mkdir /etc/apache2/ssl
mkdir -p /opt/deployer/pool
mkdir -p /opt/deployer/trash
mkdir -p /opt/deployer/deploy
sudo chown -R www-data:www-data /opt/deployer/
mkdir -p /private/var/log/apache2/
sudo cp web2py.conf /etc/apache2/sites-available/
sudo a2ensite web2py
sudo /etc/init.d/apache2 restart
```
