#!/usr/bin/python

# Python source file for prototype 11
# 7th October

import os
import json
import time
import psutil

# Shift to nodejs??
# No. Cuz python > nodejs
# directory structure planned:
# TODO: configure rwx permissions for these:
# /home/pi/data
# /home/pi/code
# /home/pi/error_log.txt

try:
    os.chdir("/home/pi/code")
except OSError, WindowsError, FileNotFoundError:
    print("Error while changing directory")
    with open("/home/pi/error_log.txt", 'a') as fobj:
        fobj.writelines([time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), "Error while changing directory\n"])
for proc in psutil.process_iter():
    pinfo = proc.as_dict(attrs=['pid', 'name'])
    #procname = str(pinfo["name"])
    ## TODO IMPORTANT - have to do mutex semaphore stuff here!!!
    ## to make sure nothing important is happening
    if procpid != str(os.getpid()):
        proc.kill()
## now replace the old files and reboot

## also have to take care of startup script to start runnning the code
## TODO? - should use docker for this??
