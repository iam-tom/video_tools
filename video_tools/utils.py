#!/usr/bin/env python

#
#
#
# Module contains several useful tools:
# Use as import only, not executable.
#
# -- assert_dir(path)...........checks if dir exists under path and establishes
#                                it if necessary.
#____________________________________________________________________
# TODO:
#
#
#
#

import os







class assert_dir():
    def __init__(self,path):
        chk = os.path.isdir(path)
        if chk == False:
           cmd="mkdir -p "+path
           os.system(cmd)

