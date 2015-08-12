# Copyright (c) 2008 Roi Dayan
# This file is part of the pyMisron project.
# http://pymisron.googlecode.com

import appuifw,e32
import sys, os

pyMisron_dir=os.getcwd()
pyMisron_libdir = '%s\lib' %pyMisron_dir
sys.path.append(pyMisron_libdir)

applock=None
txtLog=None
from interface import *

def main():
    try:
        applock = create_interface()
        post_load()
        applock.wait()
    except:
        harness()

if __name__=='__main__':
    main()
