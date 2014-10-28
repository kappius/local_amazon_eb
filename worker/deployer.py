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
logging.basicConfig(filename='debug.log', filemode='a+', level=logging.DEBUG)

# Helper functions

def post_install():
    """Execute post installation script"""
    log = ''
    if POST_INSTALL_NAME:
        log += scp.get(POST_INSTALL_PATH, ROOT)
        subprocess.Popen(os.path.join(ROOT, POST_INSTALL_NAME))
        log += process.communicate()[0]
    return log

def add_envvars():
    """Add envvars to apache"""
    log = ''
    log += scp.get(ENVVAR_PATH, ROOT)
    with open(os.path.join(ROOT, ENVVAR_NAME), 'r') as env_vars:
        with open(APACHE_ENVVARS, 'a') as sys_envvars:
            for env_var in env_vars:
                log += sys_envvars.write('export %s' % env_var)
    return log

def zip_to_deploy(f):
    """Get zip file and make deploy in correct folder"""
    log = ''
    with zipfile.ZipFile(os.path.join(POOL, f)) as zip:
        log += zip.extractall(DEPLOY)
    process = subprocess.Popen(['pip', 'install', '-r', os.path.join(DEPLOY, 'requirements.txt')], stdout=subprocess.PIPE, shell=True)
    log += process.communicate()[0]
    log += shutil.move(os.path.join(POOL, f), TRASH)
    process = subprocess.Popen(['chown', '-R', 'www-data:www-data', DEPLOY], stdout=subprocess.PIPE, shell=True)
    log += process.communicate()[0]
    return log

def restart_server():
    """Restart worker server"""
    subprocess.Popen(['shutdown', '-r', 'now'], shell=True)
    log += process.communicate()[0]
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
