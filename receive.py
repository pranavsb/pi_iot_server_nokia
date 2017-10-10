#!/usr/bin/python

# Python source file for prototype 11
# 7th October

import re
import requests
import os
import json
import time
import psutil
import hashlib


# Shift to nodejs??
# No. Cuz python > nodejs

def cmp_versions(version_str_1, version_str_2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    if normalize(version_str_1) == normalize(version_str_2):
        return 0
    elif normalize(version_str_1) > normalize(version_str_2):
        return 1
    elif normalize(version_str_1) < normalize(version_str_2):
        return -1

#TODO TESTING
def validate_json():
    new_json = json.load(open("/home/pi/code/main.json", 'r'))
    old_json = json.load(open("/home/pi/backup/main.json", 'r'))
    if cmp_versions(new_json["version"], old_json["version"]) < 0:
        with open("/home/pi/data/error_log.txt", 'a') as fobj:
            fobj.writelines([time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), "Error while checking versions\n"])
    file_list = new_json["sources"]; hash_list = new_json["sha256"]
    for source_file, hash_val in zip(file_list, hash_list):
        fobj = open(source_file, 'r')
        if hashlib.sha256(fobj.read()) != hash_val:
            with open("/home/pi/data/error_log.txt", 'a') as fobj:
                fobj.writelines([time.strftime("%b %d %Y %H:%M:%S   ", time.localtime(time.time())), "Error with sha256 values\n"])
            break



# directory structure planned:
# TODO: configure rwx permissions for these:
# /home/pi/data
# /home/pi/code
# /home/pi/data/error_log.txt
# /home/pi/backup
# /home/pi/

try:
    os.chdir("/home/pi/code")
except OSError as e:
    print("Error while changing directory")
    with open("/home/pi/data/error_log.txt", 'a') as fobj:
        fobj.writelines([time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), "Error while changing directory\n"])
except FileNotFoundError as e:
    print("Error while changing directory")
    with open("/home/pi/data/error_log.txt", 'a') as fobj:
        fobj.writelines([time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), "Error while changing directory\n"])

# TODO: unzip code.zip


# TODO: validation of json data
retval = validate_json()

def terminate_processes():
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
