#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import subprocess
import time
import math



class rendertest (object):

    def __init__(self,in_path,out_path):
        self.in_path = in_path
        self.out_path = out_path    
#        self.avconv_command = "avconv -i "+self.in_path+" "+self.out_path
#        self.erase_command = "rm "+out_path
        self.avconv_command = ["avconv","-i",self.in_path, self.out_path]
        self.erase_command = ["rm",self.out_path]

        
        self.l = list()
        print "rendertest ready to rumble"
    def run(self,n):
        n_runner = 1
        while n_runner <=n:
            t0 = time.time()
            subprocess.call(self.avconv_command)
#            os.system(self.avconv_command)
            t1 = time.time()
            dt= t1-t0
            self.l.append(dt)
            print "____________________________________"
            print "Loop %i of %i_______  %f [s]" %(n_runner,n,dt)
#            os.system(self.erase_command)
            subprocess.call(self.erase_command)
            n_runner = n_runner+1
        
    def analyse(self):
        n= len(self.l)
        s = sum(self.l)
        m = s/n
        print "\n\n________________Analysis_____________________\n"
        print "Setup:\n"
        print "From: %s"%self.in_path
        print "To  : %s\n"%self.out_path
        print "Number of samples  = %i"%n
        print "Arithmetic mean    = %f [s]" %m
        V2=0
        for i in self.l:
            v2i=(i -m) * (i-m)
            V2 = V2+v2i
        if (n-1)==0:
            print "no standard deviation "
        else:    
            sigma = math.sqrt(V2/(n-1))
            print "std. dev       = %f [s]" %sigma


if __name__ == '__main__':
#string configuration for use of os.system(...)
#    i = "/host/MEDIA/photography/2012-04-20\ SPAIN/sunrise/lapse0/lapse0_%3d.jpg"
#    o = "/host/MEDIA/photography/2012-04-20\ SPAIN/render.mov"
#string configuration for use of subprocess.call(...)
    i = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/lapse0_%3d.jpg"

    o = "/media/work/render.mov"
   
    
    test = rendertest(i,o)
    test.run(10)
    test.analyse()

