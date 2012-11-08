import sys
import os
#|----------------------------------------------------------------------------|
# | Module Name: project_config
# | Creation Date: 2012/09/05 - 
# | Author: iam-tom
# | Description: Module loads settings for specific project.Store in same folder
# |              as module in which import  is  needed or install it.
# |----------------------------------------------------------------------------|

class path_config():
#|----------------------------------------------------------------------------|
# | Class  Name: path_config
# | Creation Date: 2012/09/05 - 
# | Author: iam-tom
# | Description: Module adds paths to sys.path in order to enable structuring
# |              of the project into different subfolders.
# | Usage: Insert paths you want to add either to add paths list or to separate
# |        file. Initialize with filename.
# |----------------------------------------------------------------------------|
    def __init__(self,path_file ="NOT_SET"):

        add_paths=list()

        #check if path file is set 
        chk =  path_file in "NOT_SET"
        if chk ==False:
            # get file and parse content
            for line in open(path_file,'r').readlines():
                l=line.rstrip()
                # ignore comments
                chk = l[0] is "#"
                if chk == True:
                    continue
                else:
                    add_paths.append(l)
        # default paths -- always add
        #add_paths.append("mypy/common")


        # append add_paths to sys.path
        for p in add_paths:

            # check if path is valid dir
            chk = os.path.isdir(p)
            if chk == True:
                # modify sys.path
                sys.path.append(p)
            else:
                print "ERROR: Could not append %s to sys.path - no valid directory." % p

    def show(self):
        print sys.path








