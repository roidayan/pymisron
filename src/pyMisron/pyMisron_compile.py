# Copyright (c) 2008 Roi Dayan
# This file is part of the pyMisron project.
# http://pymisron.googlecode.com

import py_compile
import os
import time
import shutil

root=os.getcwd()
print root

py_compile.compile(root+"\pyMisron.py")
shutil.copy(root+"\pyMisron.pyc","compiled")
os.remove(root+"\pyMisron.pyc")

lib_files=os.listdir(root+"\lib")
print lib_files

for i in lib_files:
    fi='%s\lib\%s' %(root,i)
    i2=os.path.splitext(fi)
    if (i2[1]=='.py'):
        i2=i2[0]+'.pyc'
        print 'Compiling %s' %i
        py_compile.compile(fi)
        shutil.copy(i2,root+"\compiled\lib")
        os.remove(i2)
print "done."
time.sleep(15)
