#! /usr/bin/env python
def readme(path,config_list):

    fid=open(path,"w")
    fid.write("___________WORKING DIRECTORY______________\n\n")

    fid.write("This working directory was automatically\n")
    fid.write("created by WorkingDirectoryManager v1.0.\n\n")


    fid.write("Project Overview_________________________\n\n")

    fid.write("Project Name.................. %s\n" % config_list[0])
    fid.write("Creation Date................. %s\n" % config_list[1])
    fid.write("Author........................ %s\n" % config_list[2])
    fid.write("# of scenes................... %s\n" % config_list[3])
    fid.write("fps........................... %s\n" % config_list[4])
    fid.write("Resolution.................... %s\n\n" % config_list[5])

    fid.write("Layout_____________________________________\n\n")

# " Layout for Project %s:\n\n" % config_list[0])


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
