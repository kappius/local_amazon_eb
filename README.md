# Local Amazon EB

## Topology

![Topology](https://github.com/kappius/local_amazon_eb/blob/master/topology.png)

## INSTALL

### Supervisor

Using Centos and GIT:
```
sed -i -e "s/enabled=0/enabled=1/" /etc/yum.repos.d/CentOS-Base.repo
yum check_update
yum install curl-devel expat-devel gettext-devel openssl-devel zlib-devel gcc make
curl https://codeload.github.com/git/git/tar.gz/v2.0.1 --output git.tar.gz
tar -zxf git.tar.gz
cd git-2.0.1 && make prefix=/usr/local all
cd git-2.0.1 && make prefix=/usr/local install
rm -rf git.tar.gz git-2.0.1
make install ON=supervisor

```

#### Setup a cleaner

supervisor installation generate a clean_versions file that clean all versions deployed to each worker. It's only clean historical versions, and don't remove worker from production

### Worker
Using Ubuntu and GIT:

```
sudo apt-get install make git
make install
```
