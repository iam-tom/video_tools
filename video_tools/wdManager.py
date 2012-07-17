#! /usr/bin/env python

class Project_Creator:
#
# Layout for iProject:
# | ............. 
#
#		________________iProject_________
#		|				|	
#	______ files_____		_______post______
#	|	|	|		|		|
# _____video	audio	misc		org	_______render____
# |	|	:	|		|	|	|	|
# raw	conv	*	SF		SF	seq	video	audio
# :	:		:		:	|	:	:	
# *	*		*		*	SF	*	*
#						:
#						*
#
	def __init__(self,cfg_list):
            l= len(cfg_list)
	    self.basepath_=cfg_list[0]
            self.config_list = cfg_list[1:l]
	    
	def NewDir(self,name):
	    os.mkdir(name)


	def CreateReadme(self,name,config_list):
	    import wdReadme    

	    wdReadme.readme("README",config_list)	
 

	def CreateNewProject(self):
 	    print "creating wd"
	    # establish new working directory
	    self.NewDir(self.basepath_)

	    # enter working directory
	    os.chdir(self.basepath_)

	    # make working tree 
	    self.NewDir("files")
            self.NewDir("post")
            os.chdir("files")
	    self.NewDir("video")
            self.NewDir("audio")
            self.NewDir("misc")
            os.chdir("video")
	    self.NewDir('conv')
	    self.NewDir('raw')
            os.chdir("../../post")
            self.NewDir("org")
	    self.NewDir('render')
            os.chdir("render")
	    self.NewDir('seq')
            self.NewDir("video")
            self.NewDir("audio")
	    os.chdir(self.basepath_)

	    # create Readme file
	    self.CreateReadme(self.basepath_,self.config_list)


	#import modules

# for system calls
import os

# use module as script
if __name__ == "__main__":
    import sys
    #CreateWD((sys.argv[1]))
    x=Project_Creator(sys.argv[1])
    x.CreateNewProject()
