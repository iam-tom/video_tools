
import PIL
import subprocess
import os
from threading import Thread 

import utils

#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  THUMBNAILER //////////////
#/////////////// ///////////////  ////////////// //////////////

##
# Create thumbnail from movie stream
class thumbnailer():

    ##
    # Initialize object
    # @param self object pointer
    def __init__(self):
#//////////// Allocations ////////////////////

        ## output format
        self.format = ".png"
        ## input path
        self.i_path = str()
        ## output path
        self.o_path = str()  
        ## output frame size
        self.frame_size = ""
        
#///////////////  Interface Functions //////////////

    ##
    # Update configuration of thumbnailer
    # @param self object pointer
    # @param config Configuration mapping
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]

        
        
    ##
    # Trigger processing
    # @param self object pointer
    def Run(self):
        dot = self.i_path.find(".")
        mov_name = self.i_path[0:dot]
        o_path = self.o_path+"thb"+self.format
        utils.assert_dir(self.o_path)   

        if len(self.frame_size)>0:
            command = ["avconv","-i",self.i_path,"-vframes","1","-s",str(self.frame_size),"-y",o_path]
        else:
            command = ["avconv","-i",self.i_path,"-vframes","1","-y",o_path]

        subprocess.call(command)
    
#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  FRAME EXTRACTOR //////////////
#/////////////// ///////////////  ////////////// //////////////

##
# Extract frames from movie.
class frame_extractor ():

    ##
    # Initialize object
    # @param self object pointer
    def __init__(self):
#///////////// Thread stuff///////////////////


#/////////////// Allocations and default vaules //////////////
        ## output format
        self.format = ".png"
        ## number of leading zeros for frame naming
        self.leading_zeros = 3
        ## input path
        self.i_path = str()
        ## output path
        self.o_path = str()
        ## output directory
        self.o_dir = str()
        ## output frame size
        self.frame_size = ""
        ## output frame rate [fps]
        self.fps = 1



#/////////////// Interface Methods //////////////

    ##
    # Update configuration of thumbnailer
    # @param self object pointer
    # @param config Configuration mapping
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.leading_zeros = config["zeros"]
        self.i_path = config["i_path"]
        self.o_dir = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        


    ##
    # Trigger processing
    # @param self object pointer
    def Run(self):
#        get movie name    
        dot = self.i_path[0].find(".")
        slash = self.i_path[0].rfind("/")
        mov_name = self.i_path[0][slash+1:dot]
        self.o_path = self.o_dir+mov_name+"%"+str(self.leading_zeros)+"d"+self.format
        utils.assert_dir(self.o_dir)
        if len(self.frame_size)>0:
            command = ["avconv","-i",self.i_path[0],"-r",str(self.fps),"-s",self.frame_size,"-v","-10","-y",self.o_path]
        else:
           
            command = ["avconv","-i",self.i_path[0],"-r",str(self.fps),"-y",self.o_path]
            print command
            subprocess.call(command)            
        


#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  CONVERTER //////////////
#/////////////// ///////////////  ////////////// //////////////       
    
##
# Convert video.
class converter ():

    ##
    # Initialize object
    # @param self object pointer
    def __init__(self):
#/////////////// Allocations and default vaules //////////////
        ## output format
        self.format = ".mov"
        ## input path
        self.i_path = list()
        ## output path
        self.o_path = str()
        ## frame size
        self.frame_size = "vga"
        ## output frame rate [fps]
        self.fps = 25
        ## output bitrate [bps]
        self.bv = "3000K"
        
    ##
    # Update configuration of thumbnailer
    # @param self object pointer
    # @param config Configuration mapping
    def UpdateConfig(self,config):
        ## output format
        self.container = config["format"]
        ## input path
        self.i_path = config["i_path"]
        ## output path
        self.o_path = config["o_path"]
        ## frame size
        self.frame_size = config["frame_size"]
        ## output frame rate  [fps]
        self.fps = config["fps"]
        ## output quality [bps]
        self.q = config["bv"]

    ##
    # Trigger processing
    # @param self object pointer
    def Run(self):
    
        for i_file in self.i_path:
    #        get movie name

            dot = i_file.rfind(".")
            slash = i_file.rfind("/")
            mov_name = i_file[slash+1:dot]
            o_path = self.o_path+mov_name+"_conv"+self.container
            print o_path
            
            if len(self.frame_size)>0:
                
                command = ["avconv","-i",i_file,"-strict","experimental","-s",str(self.frame_size),"-r",self.fps,"-b:v",self.bv,o_path]
            else:
                command = ["avconv","-i",i_file,"-strict","experimental","-r",str(self.fps),"-b:v",self.bv,o_path]
                
            subprocess.call(command)       
        
    
    
 
        
#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  STREAMER //////////////
#/////////////// ///////////////  ////////////// ////////////// 

##
# Stream image sequence to video file.
class streamer ():

    ##
    # Initialize object
    # @param self object pointer
    def __init__(self):
#/////////////// Allocations and default vaules //////////////
        ## input format
        self.format = ".mov"
        ## input paths
        self.i_path = str()
        ## output path
        self.o_path = str()
        ## leading zeros in output
        self.leading_zeros = 3
        ## output frame size
        self.frame_size = ""
        ## output framerate [fps]
        self.fps = 25
        ## output bitrate [bps]
        self.q = "5000K" 

    ##
    # Update configuration of thumbnailer
    # @param self object pointer
    # @param config Configuration mapping
    def UpdateConfig(self,config):
        self.format= config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
#        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        self.leading_zeros = config["zeros"]
#        self.q = config["bv"]

    ##
    # Trigger processing
    # @param self object pointer
    def Run(self):
#        get movie name

        chk =  os.path.isdir(self.i_path)
        if chk  == True:
            allf = sorted(os.listdir(self.i_path)); 
            f = allf[0]
            dot = f.rfind(".")
            i_format = f[(dot):(len(self.i_path))]
            i_name =  f[0:(dot-self.leading_zeros)]
            i_path = self.i_path+i_name+"%"+str(self.leading_zeros)+"d"+i_format

        else:                        
                
            dot = self.i_path[0].rfind(".")
            i_format = self.i_path[0][(dot):(len(self.i_path))]
            i_name =  self.i_path[0][0:(dot-self.leading_zeros)]
            i_path = self.i_path[0][0:(dot-self.leading_zeros)]+"%"+str(self.leading_zeros)+"d"+i_format
        
        o_path = self.o_path+i_name+"_stream"+self.format
        
        if len(self.frame_size)>0:
            command = ["avconv","-r",str(self.fps),"-i",i_path,"-s",self.frame_size,"-b:v","10000K","-r",str(self.fps),o_path]
        else:
            command = ["avconv","-r",str(self.fps),"-i",i_path,"-b:v","10000K","-r",str(self.fps),o_path]
        subprocess.call(command)       
        
    
    
 








if __name__ == '__main__':



    i_path_list = list()
    i_path_list.append("test.mov")
    config={"format":".png","zeros":3,"i_path":"test.mov","o_path":"","frame_size":"vga","fps":1}
    config_c={"format":".mov","zeros":3,"i_path":i_path_list,"o_path":"","frame_size":"vga","fps":25,"bv":"10000K"}
    config_s={"format":".mov","zeros":3,"i_path":"test001.png","o_path":"","frame_size":"vga","fps":25}
    F = frame_extractor()
    T = thumbnailer()
    C = converter()
    S = streamer()
    
    F.UpdateConfig(config)
    T.UpdateConfig(config)
    C.UpdateConfig(config_c)
    S.UpdateConfig(config_s)
    
#    T.CreateThumbnail()
#    F.ExtractFrames()
#    C.Convert()
    S.Stream()


