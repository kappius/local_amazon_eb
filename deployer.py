#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, shutil, os, glob, zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import call

ROOT = '/opt/deployer/'
POOL = ROOT+'pool/'
TRASH = ROOT+'trash/'
DEPLOY = ROOT+'deploy/'

class DumpHandler(FileSystemEventHandler):
    def on_modified(self, event):

        files = glob.iglob(os.path.join(POOL, "*.zip"))
        for f in files:
            if os.path.isfile(f):
                with zipfile.ZipFile(os.path.join(POOL, f)) as zip:
                    zip.extractall(DEPLOY)
                call(['pip', 'install', '-r', os.path.join(DEPLOY, 'requirements.txt')])
                shutil.move(f, TRASH)


if __name__ == "__main__":
    event_handler = DumpHandler()
    observer = Observer()
    observer.schedule(event_handler, path=POOL, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
