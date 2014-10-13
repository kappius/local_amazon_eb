#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, shutil, os, glob, zipfile, sys
from subprocess import call
from paramiko import SSHClient
from scp import SCPClient

ROOT = os.environ['INSTALL_DIR']
POOL = os.environ['POOL_DIR']
TRASH = os.environ['TRASH_DIR']
DEPLOY = os.environ['DEPLOY_DIR']
SUPERVISOR_USER = os.environ['SUPERVISOR_USER']
SUPERVISOR_IP = os.environ['SUPERVISOR_IP']
ENVVAR_PATH = os.environ['ENVVAR_PATH']
ENVVAR_NAME = os.environ['ENVVAR_NAME']
USER_HOME = os.path.expanduser('~')

while True:
    files = glob.iglob(os.path.join(POOL, "*.zip"))
    for f in files:
        if os.path.isfile(f):
            try:
                with zipfile.ZipFile(os.path.join(POOL, f)) as zip:
                    zip.extractall(DEPLOY)
                call(['pip', 'install', '-r', os.path.join(DEPLOY, 'requirements.txt')])
                shutil.move(os.path.join(POOL, f), TRASH)
            except Exception, e:
                print e
                sys.exit()
            call(['chown', '-R', 'www-data:www-data', DEPLOY])

            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(SUPERVISOR_IP,username=SUPERVISOR_USER)

            # SCPCLient takes a paramiko transport as its only argument
            scp = SCPClient(ssh.get_transport())

            scp.get(ENVVAR_PATH, ROOT)

            with open(os.path.join(ROOT, ENVVAR_NAME), 'a') as env_vars:
                with open(os.path.join(USER_HOME, '.bashrc'), 'a') as bashrc:
                    for env_var in env_vars:
                        bashrc.write('export %s' % env_var)
            call(['source', os.path.join(USER_HOME, '.bashrc')])
            sys.exit()
    time.sleep(1)
