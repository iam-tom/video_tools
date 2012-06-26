#! /usr/bin/env python

class wdm:
	def __init__(self,basepath,cfg_list):

	    self.basepath_=basepath
            self.config_list = cfg_list
	    
	def NewDir(self,name):
	    os.mkdir(name)


	def CreateReadme(self,name,config_list):
	    import generic_text    

	    generic_text.readme("README",config_list)	
 

	def CreateWD(self):
 	    print "creating wd"
	    # establish new working directory
	    self.NewDir(self.basepath_)

	    # enter working directory
	    os.chdir(self.basepath_)

	    # make working directory default layout  
	    self.NewDir('conv')
	    self.NewDir('raw')
	    self.NewDir('render')
	    self.NewDir('seq')

	    # create Readme file
	    self.CreateReadme(self.basepath_,self.config_list)


	#import modules

# for system calls
import os

# use module as script
if __name__ == "__main__":
    import sys
    #CreateWD((sys.argv[1]))
    x=wdm(sys.argv[1])
    x.createWD()
