#! /usr/bin/env python
import wdGenericText
import wdManager    
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
	def __init__(self,cfg_list,vcfg_list):
            self.wd = wdManager.wd_cfg() 
            self.wd.basepath=cfg_list.basepath
            self.wd.name    =cfg_list.name

            self.vcfg = wdManager.vid_cfg()
            self.vcfg.basepath = vcfg_list.basepath
            self.vcfg.name       = vcfg_list.name
            self.vcfg.author     = vcfg_list.author
            self.vcfg.res        = vcfg_list.res
            self.vcfg.fps        = vcfg_list.fps
            self.vcfg.desc       = vcfg_list.desc

	    
	def NewDir(self,name):
	    os.mkdir(name)


	def CreateReadme(self,name,config_list):


	    wdGenericText.readme("README",config_list)

        def CreateWDFile(self,config_list):
            wdGenericText.wdfile(".wd",config_list)	
 

	def CreateNewProject(self):
 	    print "creating wd"
	    # establish new working directory
	    self.NewDir(self.wd.basepath)

	    # enter working directory
	    os.chdir(self.wd.basepath)

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
	    os.chdir(self.wd.basepath)

	    # create Readme file
	    self.CreateReadme(self.wd.basepath,self.vcfg)
            self.CreateWDFile(self.vcfg)


	#import modules
class wd_cfg:
    def __init__(self):
        self.basepath= ""
        self.name = ""

class vid_cfg:
    def __init__(self):
        self.basepath=""
        self.date   = ""
        self.name   =""
        self.author = ""
        self.scenes = ""
        self.fps    =""
        self.res    = ""
        self.desc   = ""
 

# for system calls
import os

# use module as script
if __name__ == "__main__":
    import sys
    #CreateWD((sys.argv[1]))
    x=Project_Creator(sys.argv[1])
    x.CreateNewProject()
