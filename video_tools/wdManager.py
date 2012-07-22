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
	def __init__(self):
            print "[DBG] still useful ?"
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

	    
	def NewDir(self,dirname):
	    os.mkdir(dirname)


	def CreateReadme(self,WD):
	    wdGenericText.readme(WD)

        def CreateWDFile(self,WD):
            wdGenericText.wdfile(WD)	

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
            cwd = os.getcwd()
            if  WD.old_wd == True and WD.name in WD.basepath:
                print "old wd accepted" 
            elif WD.old_wd ==True and  not WD.name in WD.basepath :
                print "renaming.."
                os.chdir(WD.basepath)
                os.chdir("../")
                os.rename(WD.basepath, WD.name)
            # make WD consistent
                a= WD.basepath
                counter = 0
                while a.find("/") <> -1:
                    b=a.find("/")
                    a=a[b+1:len(a)]
                    counter = counter+(b+1)
                WD.basepath = WD.basepath[0:counter]+WD.name
            # write updated .wd file
                self.CreateWDFile(WD)

            elif WD.old_wd == False :
                print "creating new wd"
                
	        # establish new working directory
	        self.NewDir(WD.basepath)

                # enter working directory
	        os.chdir(WD.basepath)

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
	        os.chdir(WD.basepath)

	        # create Readme file
	        self.CreateReadme(WD)
                self.CreateWDFile(WD)
                
                # return to original path
                os.chdir(cwd)

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
        self.done   = False
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
