# Copyright (c) 2008 Roi Dayan
# This file is part of the pyMisron project.
# http://pymisron.googlecode.com

import e32
import sys, os

python_dir = '\Python'
pyMisron_dir = '%s\pyMisron' %python_dir

if e32.in_emulator():
    pys60rcPath = 'C:%s' %pyMisron_dir
else:
    pys60rcPath = 'E:%s' %pyMisron_dir

os.chdir(pys60rcPath)
sys.path.append(pys60rcPath)

import pyMisron
pyMisron.main()
