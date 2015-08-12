# Copyright (c) 2008 Roi Dayan
# This file is part of the pyMisron project.
# http://pymisron.googlecode.com

#control configuration
#init_settings      - called from read_settings if needed.
#read_settings      - set settings variable.
#update_settings    - update settings.
#write_settings     - write settings variable.

my_config_file = "settings.txt"
my_config = my_config_file

#default_settings = {'icq_gateway': 'http://misron.net/send/index.php', 'icq_login': None, 'icq_password': None, 'default_ap': None,
#                    'proxy': None, 'proxy_ap': None, 'default_areacode': None, 'alias': None}

default_settings = {'icq_gateway': 'http://misron.net/send/index.php', 'icq_logins': {}, 'default_ap': None,
                    'proxy': None, 'proxy_ap': None, 'default_areacode': None, 'alias': None}

import codecs
from interface import *

def init_settings():
    global settings
    read_settings()
    #make sure we got all default settings
    count_add=0
    for item in default_settings:
        if not settings.has_key(item):
            settings[item]=default_settings[item]
            count_add+=1
    #delete obsolete settings
    count_rem=0
    tmpsets=settings.copy()
    for item in tmpsets:
        if not default_settings.has_key(item):
            settings.__delitem__(item)
            count_rem+=1
    #rewrite configuration
    if count_add>0 or count_rem>0:
        write_settings()

def reset_all_settings():
    global settings
    settings = default_settings
    write_settings()

def read_settings():
    global settings
    try:
        f = open(my_config,'rt')
        #f = codecs.open(my_config, 'r', 'utf-8')
        data = f.read()
        f.close()
        settings = eval(data)
    except:
        reset_all_settings()

def update_settings(key, val = None):
    global settings
    if val == None and settings.has_key(key):
            settings.pop(key)
    else:
        settings[key] = val;

def write_settings(key = None, val = None):
    global settings
    if key != None:
        if val == None and settings.has_key(key):
            settings.pop(key)
        else:
            settings[key] = val;
    try:
        f = open(my_config,'wt')
        #f = codecs.open(my_config, 'w', 'utf-8')
        f.write(repr(settings))
        f.close()
    except:
        raise Exception, "Error writing configuration file"

#init
init_settings()
