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
class tuple_op():
    def __init__(self,t):
        self.tup=t 
    def mul(self,factor):
        res=tuple([int(factor*i) for i in self.tup])
        return res
    def div(self,factor):
        res=tuple([i/factor for i in self.tup])
        return res
