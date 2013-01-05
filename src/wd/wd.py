#! /usr/bin/env python
class Project_Creator:
#
# Layout for iProject:
# | ............. 
#
#        ________________iProject_________
#        |                |    
#    ______ files_____        _______post______
#    |    |    |        |        |
# _____video    audio    misc        org    _______render____
# |    |    :    |        |    |    |    |
# raw    conv    *    SF        SF    seq    video    audio
# :    :        :        :    |    :    :    
# *    *        *        *    SF    *    *
#                        :
#                        *
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
        self.readme(WD)

    def CreateWDFile(self,WD):
        self.wdfile(WD)    

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
            self.NewDir("photo")
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



    def readme(self,WD):
        os.chdir(WD.basepath)
        fid=open("README","w")
        fid.write("___________WORKING DIRECTORY______________\n\n")
    
        fid.write("This working directory was automatically\n")
        fid.write("created by WorkingDirectoryManager v1.0.\n\n")
    
    
        fid.write("Project Overview_________________________\n\n")
    
        fid.write("Project Name.................. %s\n" % WD.name)
        fid.write("Creation Date................. %s\n" % WD.date)
        fid.write("Author........................ %s\n" % WD.author)
        fid.write("# of scenes................... %s\n" % WD.scenes)
        fid.write("fps........................... %s\n" % WD.fps)
        fid.write("Resolution.................... %s\n\n" % WD.res)
    
        fid.write("Layout_____________________________________\n\n")
    
    # " Layout for Project %s:\n\n" % WD[0])
    
    
        fid.write("\t\t________________iProject_________\n")
        fid.write("\t\t|\t\t\t\t|\n")    
        fid.write("\t______ files_____\t\t_______post______\n")
        fid.write("\t|\t|\t|\t\t|\t\t|\n")
        fid.write("_____video\taudio\tmisc\t\torg\t_______render____\n")
        fid.write("|\t|\t:\t|\t\t|\t|\t|\t|\n")
        fid.write("raw\tconv\t*\tSF\t\tSF\tseq\tvideo\taudio\n")
        fid.write(":\t:\t\t:\t\t:\t|\t:\t:\n")    
        fid.write("*\t*\t\t*\t\t*\tSF\t*\t*\n")
        fid.write("\t\t\t\t\t\t:\n")
        fid.write("\t\t\t\t\t\t*\n")
        
        fid.write("files ............................... file stock contained in this project\n")
        fid.write("files/raw ........................... Raw files directly from camera\n")
        fid.write("files/conv .......................... converted video files\n")
        fid.write("files/conv .......................... audio files used in project\n")
        fid.write("post ................................ data created during post processing\n")
        fid.write("post/org ............................ project structures from external programms\n")
        fid.write("post/render ......................... rendered data\n")
        fid.write("post/render/seq ..................... rendered image sequences\n")
        fid.write("post/render/video ................... rendered videos\n")
        fid.write("post/render/audio ................... rendered audio files\n")
        fid.close()
    
    def wdfile(self,WD):
        os.chdir(WD.basepath)
        fid=open(".wd","w")
        fid.write("\n")
    
    
        fid.write("$name \n%s\n" % WD.name)
        fid.write("$date \n%s\n" % WD.date)
        fid.write("$scenes \n%s\n" % WD.scenes)
        fid.write("$author \n%s\n" % WD.author)
        fid.write("$fps \n%s\n" % WD.fps)
        fid.write("$res \n%s\n" % WD.res)
     
        fid.close()


 

# for system calls
import os

# use module as script
if __name__ == "__main__":
    import sys
    #CreateWD((sys.argv[1]))
    x=Project_Creator(sys.argv[1])
    x.CreateNewProject()


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
