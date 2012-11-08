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



class temp_dir_handler():
    def __init__(self):
        self.dirs_pers=list()
        self.dirs_trans=list()
    def add_dir(self,path,mode="TRANS"):
        assert_dir(path)
        if mode is "TRANS":
            self.dirs_trans.append(path)
        elif mode is "pre-clean":
            self.dirs_trans.append(path)
            self.clean()
            self.add_dir(path)
        elif mode is "PERS":
            self.dirs_pers.append(path)
    def clean(self):
        for p in self.dirs_trans:
            os.system("rm -rf %s"%p)
            self.dirs_trans[:]=[]
   


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
##
# Matrix multiplation for 3x3 matrices given as 1,9 tuple    
def mat_mul3x3(a,b):
    r0=a[0]*b[0]+a[1]*b[3]+a[2]*b[6]
    r1=a[0]*b[1]+a[1]*b[4]+a[2]*b[7]
    r2=a[0]*b[2]+a[1]*b[5]+a[2]*b[8]
    r3=a[3]*b[0]+a[4]*b[3]+a[5]*b[6]
    r4=a[3]*b[1]+a[4]*b[4]+a[5]*b[7]
    r5=a[3]*b[2]+a[4]*b[5]+a[5]*b[8]
    r6=a[6]*b[0]+a[7]*b[3]+a[8]*b[6]
    r7=a[6]*b[1]+a[7]*b[4]+a[8]*b[7]
    r8=a[6]*b[2]+a[7]*b[5]+a[8]*b[8]
    return (r0,r1,r2,r3,r4,r5,r6,r7,r8)        
def zero_str(n_zeros,i):
    
    i_str=str(i)
    zero_str=str()
    for n in range(n_zeros):
        zero_str+="0"
    zero_str=zero_str[0:len(zero_str)-len(i_str)]+i_str
    return zero_str
