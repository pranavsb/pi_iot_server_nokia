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

TIMEOUT = 5  # time in seconds to sleep
URL = "http://192.168.43.57:3000/redcode"  # address of server

def cmp_versions(version_str_1, version_str_2):
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    if normalize(version_str_1) == normalize(version_str_2):
        return 0
    elif normalize(version_str_1) > normalize(version_str_2):
        return 1
    elif normalize(version_str_1) < normalize(version_str_2):
        return -1

def write_to_error_log(string_list):
    with open("/home/pi/data/error_log.txt", 'a') as fobj:
        fobj.writelines([time.strftime("%b %d %Y %H:%M:%S   ", time.localtime(time.time()))] + string_list)

def validate_json():
    new_json = json.load(open("/home/pi/code/main.json", 'r'))
    old_json = json.load(open("/home/pi/backup/main.json", 'r'))
    if cmp_versions(new_json["version"], old_json["version"]) < 0:
        write_to_error_log(["Error while checking versions\n"])
        return False
    file_list = new_json["sources"]; hash_list = new_json["sha256"]
    for source_file, hash_val in zip(file_list, hash_list):
        fobj = open(source_file, 'r')
        if hashlib.sha256(fobj.read()) != hash_val:
            write_to_error_log(["Error with sha256 values\n"])
            return False
    #TODO set timeout - write to file like config.txt?
    time.sleep(TIMEOUT)
    #TODO verify key
    write_to_error_log(["JSON validated successfully\n"])
    return True

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
    write_to_error_log(["Error while changing directory\n"])
except FileNotFoundError as e:
    print("Error while finding files")
    write_to_error_log(["Error while finding files\n"])

# TODO code to ping server for code updates and other networking stuff

retval = validate_json()
if retval == True:
    try:
        os.chdir("/home/pi")
        os.run("rm -r /home/pi/backup/")
        os.run("mkdir /home/pi/backup")
        os.run("cp -r /home/pi/code/. /home/pi/backup/.")
        write_to_error_log(["Previous version backed up successfully\n"])
        terminate_processes(TIMEOUT)
        os.run("rm -r /home/pi/code")
        os.system("unzip code.zip")
    except OSError as e:
        print("Error while changing directory")
        write_to_error_log(["Error while changing directory\n"])
    except FileNotFoundError as e:
        print("Error while finding files")
        write_to_error_log(["Error while finding files\n"])
else:
    write_to_error_log(["Error with JSON validation\n"])


def terminate_processes(TIMEOUT):
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'name'])
        #procname = str(pinfo["name"])
        ## TODO IMPORTANT - have to do mutex semaphore stuff here!!!
        while True:
            with open("/home/pi/code/running.txt") as fobj:
                if int(fobj.read()) == 0:
                    # safe to end processes
                    break
            time.sleep(TIMEOUT)
            with open("/home/pi/data/error_log.txt", 'a') as fobj:
                fobj.writelines([time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), "Error with terminating processes\n"])

        ## to make sure nothing important is happening
        if procpid != str(os.getpid()):
            proc.kill()
## now replace the old files and reboot

## also have to take care of startup script to start runnning the code
## TODO? - should use docker for this??
