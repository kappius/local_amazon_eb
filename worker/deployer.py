#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, shutil, os, glob, zipfile, sys, logging, subprocess
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

# Define env vars
ROOT = os.environ['INSTALL_DIR']
POOL = os.environ['POOL_DIR']
TRASH = os.environ['TRASH_DIR']
DEPLOY = os.environ['DEPLOY_DIR']
SUPERVISOR_USER = os.environ['SUPERVISOR_USER']
SUPERVISOR_IP = os.environ['SUPERVISOR_IP']
ENVVAR_PATH = os.environ['ENVVAR_PATH']
ENVVAR_NAME = os.environ['ENVVAR_NAME']
POST_INSTALL_PATH = os.environ['POST_INSTALL_PATH']
POST_INSTALL_NAME = os.environ['POST_INSTALL_NAME']
APACHE_ENVVARS = '/etc/apache2/envvars'

# Define ssh connection to supervisor
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(SUPERVISOR_IP,username=SUPERVISOR_USER)

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

# Make log file
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Helper functions

def post_install():
    """Execute post installation script"""
    log = ''
    if POST_INSTALL_NAME:
        scp.get(POST_INSTALL_PATH, ROOT)
        log += subprocess.check_output([os.path.join(ROOT, POST_INSTALL_NAME)])
    return log

def add_envvars():
    """Add envvars to apache"""
    try:
        scp.get(ENVVAR_PATH, ROOT)
        with open(os.path.join(ROOT, ENVVAR_NAME), 'r') as env_vars:
            with open(APACHE_ENVVARS, 'a') as sys_envvars:
                for env_var in env_vars:
                    sys_envvars.write('export %s' % env_var)
    except Exception as e:
        return e

def zip_to_deploy(f):
    """Get zip file and make deploy in correct folder"""
    log = ''
    with zipfile.ZipFile(os.path.join(POOL, f)) as zip:
        zip.extractall(DEPLOY)
    log += subprocess.check_output(['pip', 'install', '-r', os.path.join(DEPLOY, 'requirements.txt')])
    shutil.move(os.path.join(POOL, f), TRASH)
    log += subprocess.check_output(['chown', '-R', 'www-data:www-data', DEPLOY])
    return log

def restart_server():
    """Restart worker server"""
    log += subprocess.check_output(['shutdown', '-r', 'now'])
    return log

# Start loop waiting zip
while True:
    files = glob.iglob(os.path.join(POOL, "*.zip"))
    for f in files:
        if os.path.isfile(f):
            
            logging.debug(zip_to_deploy(f))

            logging.debug(add_envvars())

            logging.debug(post_install())

            logging.debug(restart_server())

    time.sleep(1)
