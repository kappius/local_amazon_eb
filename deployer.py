#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, shutil, os, glob
from modules import mail
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import check_output
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/home/ubuntu/medk/importador/config.ini')

ROOT = config.get('paths', 'root')
POOL = ROOT+config.get('paths', 'pool')
TRASH = ROOT+config.get('paths', 'trash')
BACKUP = ROOT+config.get('paths', 'backup')

HOST = config.get('banco', 'host')
USER = config.get('banco', 'user')
PASS = config.get('banco', 'pass')

class DumpHandler(FileSystemEventHandler):
    def on_moved(self, event):
        try:
            output = check_output("bash scripts/backup.sh -p %s -b %s -h %s -u %s -P %s" %(POOL,
                                                                                           BACKUP,
                                                                                           HOST,
                                                                                           USER,
                                                                                           PASS),
                                  shell=True)
        except Exception as e:
            mail.send(str(e))
            raise e
        try:
            output = check_output("bash scripts/import.sh -p %s -h %s -u %s -P %s" %(POOL,
                                                                                     HOST,
                                                                                     USER,
                                                                                     PASS),
                                  shell=True)

        except Exception as e:
            try:
                output = check_output("bash scripts/restore.sh -p %s -b %s -h %s -u %s -P %s" %(POOL,
                                                                                                BACKUP,
                                                                                                HOST,
                                                                                                USER,
                                                                                                PASS),
                                  shell=True)

            except Exception as e:
                mail.send(str(e))
                raise e
            mail.send(str(e))
            raise e

        files = glob.iglob(os.path.join(POOL, "*.did"))
        for f in files:
            if os.path.isfile(f):
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
