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
import math






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


class split_seq():
    def __init__(self,paths,parts):
        l=len(paths)
        print l
        self.indices=list()
        if l%parts == 0:
            for i in range(parts):
                self.indices.append(i* l/parts)
        else:
            for i in range(parts):
                self.indices.append(int(math.ceil(i * l/parts)))
    def get_indices(self):
        return self.indices
    
        
