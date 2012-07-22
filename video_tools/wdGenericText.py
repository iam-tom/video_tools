#! /usr/bin/env python
def readme(WD):

    fid=open(WD.basepath,"w")
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

def wdfile(WD):
    
    fid=open(WD.basepath,"w")
    fid.write("\n")


    fid.write("$name %s\n" % WD.name)
    fid.write("$date %s\n" % WD.date)
    fid.write("$scenes %s\n" % WD.scenes)
    fid.write("$author %s\n" % WD.author)
    fid.write("$fps %s\n" % WD.fps)
    fid.write("$res %s\n" % WD.res)
 
    fid.close()

