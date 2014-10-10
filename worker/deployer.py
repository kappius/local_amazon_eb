#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, shutil, os, glob, zipfile, sys
from subprocess import call

ROOT = os.environ['INSTALL_DIR']
POOL = os.environ['POOL_DIR']
TRASH = os.environ['TRASH_DIR']
DEPLOY = os.environ['DEPLOY_DIR']

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
            call(['scp', '%s@%s:%s' %(SUPERVISOR_USER, SUPERVISOR_IP, ENVVAR_PATH), DEPLOY])
            call(['sed', '-i', 's/\(\(.*\)\)/export \1/', os.path.join(DEPLOY, ENVVAR_NAME)])
            call('cat', [os.path.join(DEPLOY, ENVVAR_NAME), '>>', '~/.bashrc'])
            call('source', '~/.bashrc')
            sys.exit()
    time.sleep(1)
