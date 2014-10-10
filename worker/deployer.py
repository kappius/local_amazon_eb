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
                continue
            call(['chown', '-R', 'www-data:www-data', DEPLOY])
            sys.exit()
    time.sleep(1)
