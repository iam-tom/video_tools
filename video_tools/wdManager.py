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
	def __init__(self,WD):
            self.WD=WD
            #self.wd = wdManager.wd_cfg() 
            #self.wd.basepath=cfg_list.basepath
            #self.wd.name    =cfg_list.name

            #self.vcfg = wdManager.vid_cfg()
            #self.vcfg.basepath = vcfg_list.basepath
            #self.vcfg.name       = vcfg_list.name
            #self.vcfg.author     = vcfg_list.author
            #self.vcfg.res        = vcfg_list.res
            #self.vcfg.fps        = vcfg_list.fps
            #self.vcfg.desc       = vcfg_list.desc

	    
	def NewDir(self,WD):
	    os.mkdir(WD.name)


	def CreateReadme(self,WD):
	    wdGenericText.readme("README",WD)

        def CreateWDFile(self,WD):
            wdGenericText.wdfile(".wd",WD)	

        def ReadWDFile(self,WD):
            fid = open(".wd")
            tag = ""
            for line in fid:
                if "$" in line:	
                    tag =line[1:len(line)]
                    continue
                else:                        
                    WD.set_attribute(tag,line)
            
                    
                    
                    

	def CreateNewProject(self,WD): 	    
	    #check if old WD
            if WD.old_wd ==True && WD.name in WD.basepath == False:
                os.chdir(WD.basepath)
                os.chdir("../")
                os.rename(WD.basepath WD.name)
            else:
                
	    # establish new working directory
	    self.NewDir(self.WD.basepath)

	    # enter working directory
	    os.chdir(self.WD.basepath)

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
	    self.CreateReadme(self.WD)
            self.CreateWDFile(self.WD)


	#import modules
class wd_cfg:
    def __init__(self):
        self.basepath=""
        self.date   = ""
        self.name   =""
        self.author = ""
        self.scenes = ""
        self.fps    =""
        self.res    = ""
        self.desc   = ""
        self.old_wd = False
    def set_attribute(self,att,val):
        if "name" in att:
            print "name set"
            self.name = val

        elif "date" in att:
            print "date set"
            self.date = val

        elif "author" in att:
            print "author set"
            self.author = val

        elif "basepath" in att:
            print "basepath set"
            self.basepath = val

        elif "res" in att:
            print "res set"
            self.res = val

        elif "scenes" in att:
            print "scenes set"
            self.scenes = val
        elif "fps" in att:
            print "fps set"
            self.fps = val


        else:
            print "tag %s not implemented" % att


 

# for system calls
import os

# use module as script
if __name__ == "__main__":
    import sys
    #CreateWD((sys.argv[1]))
    x=Project_Creator(sys.argv[1])
    x.CreateNewProject()
