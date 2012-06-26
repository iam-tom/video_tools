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

    fid.write("Project tree_____________________________________\n\n")

    fid.write("raw........................... Raw files directly from camera\n")
    fid.write("conv.......................... converted files\n")
    fid.write("seq........................... rendered image sequences\n")
    fid.write("render........................ rendered videos\n")
    fid.close()
