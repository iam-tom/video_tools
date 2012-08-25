#!/usr/bin/env python
#-*- coding:utf-8 -*-

import PIL
import subprocess
import os
import threading

import utils


#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  THUMBNAILER //////////////
#/////////////// ///////////////  ////////////// //////////////

class thumbnailer():

    def __init__(self):
#//////////// Allocations ////////////////////
#        self.config = list()
#        self.thumb = PIL.Image()
        self.format = ".png"
        self.i_path = str()
        self.o_path = str()
        self.frame_size = ""



        
        
#///////////////  Interface Functions //////////////
 
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]

        
        
    def Run(self):
#        get movie name    
        dot = self.i_path.find(".")
        mov_name = self.i_path[0:dot]
#        o_path = self.o_path+mov_name+"_thb"+self.format
        o_path = self.o_path+"thb"+self.format
    
        #if os.path.isdir(self.o_path) == False:
        #    mkdir_str = "mkdir -p "+self.o_path
        #    os.system(mkdir_str)

        if len(self.frame_size)>0:
            command = ["avconv","-i",self.i_path,"-vframes","1","-s",str(self.frame_size),"-y",o_path]
        else:
            command = ["avconv","-i",self.i_path,"-vframes","1","-y",o_path]

        subprocess.call(command)

        
        
#/////////////// Internal Methods //////////////
    def load_thumbnail(self):
        print "to be implemented"
#        function loads the thumbnail and saves it as a PIL.IMAGE
    
 
 
 
    
#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  FRAME EXTRACTOR //////////////
#/////////////// ///////////////  ////////////// //////////////


class frame_extractor ():

    def __init__(self):
#/////////////// Allocations and default vaules //////////////
        self.format = ".png"
        self.leading_zeros = 3
        self.i_path = str()
        self.o_path = str()
        self.o_dir = str()
        self.frame_size = ""
        self.fps = 1



#/////////////// Interface Methods //////////////

    def UpdateConfig(self,config):
        self.format = config["format"]
        self.leading_zeros = config["zeros"]
        self.i_path = config["i_path"]
        self.o_dir = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        
    

    def Run(self):
#        get movie name    
        dot = self.i_path[0].find(".")
        slash = self.i_path[0].rfind("/")
        mov_name = self.i_path[0][slash+1:dot]
        self.o_path = self.o_dir+mov_name+"%"+str(self.leading_zeros)+"d"+self.format
        utils.assert_dir(self.o_dir)
        #if os.path.isdir(self.o_path) == False:
        #    mkdir_str = "mkdir -p "+self.o_dir
        #    os.system(mkdir_str)
        self.exe()
    def exe(self):    
        if len(self.frame_size)>0:
            command = ["avconv","-i",self.i_path[0],"-r",str(self.fps),"-s",self.frame_size,"-v","-10","-y",self.o_path]
        else:
           
            command = ["avconv","-i",self.i_path[0],"-r",str(self.fps),"-y",self.o_path]
            print command
            subprocess.call(command)            
        


#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  CONVERTER //////////////
#/////////////// ///////////////  ////////////// //////////////       
    
class converter ():

    def __init__(self):
#/////////////// Allocations and default vaules //////////////
        self.format = ".mov"
        self.i_path = list()
        self.o_path = str()
        self.frame_size = "vga"
        self.fps = 25
        self.bv = "3000K"
        
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        self.q = config["bv"]

    def Run(self):
    
        for i_file in self.i_path:
    #        get movie name

            dot = i_file.rfind(".")
            slash = i_file.rfind("/")
            mov_name = i_file[slash+1:dot]
            o_path = self.o_path+mov_name+"_conv"+self.format
            

            command = ["avconv","-i",i_file,"-strict","experimental","-s",self.frame_size,"-r",str(self.fps),"-b:v",self.bv,o_path]
            subprocess.call(command)       
        
    
    
 
        
#/////////////// /////////////////////////// //////////////
#/////////////// CLASS:  STREAMER //////////////
#/////////////// ///////////////  ////////////// ////////////// 

class streamer ():

    def __init__(self):
#/////////////// Allocations and default vaules //////////////
        self.format = ".mov"
        self.i_path = str()
        self.o_path = str()
        self.leading_zeros = 3
        self.frame_size = ""
        self.fps = 25
        self.q = "5000K" 
    def UpdateConfig(self,config):
        self.format= config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
#        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        self.leading_zeros = config["zeros"]
#        self.q = config["bv"]

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


