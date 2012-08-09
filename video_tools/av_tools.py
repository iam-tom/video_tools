#!/usr/bin/env python
#-*- coding:utf-8 -*-

import PIL
import subprocess


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
        self.frame_size = "vga"



        
        
#///////////////  Interface Functions //////////////
 
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]

        
        
    def CreateThumbnail(self):
#        get movie name    
        dot = self.i_path.find(".")
        mov_name = self.i_path[0:dot]
        o_path = self.o_path+mov_name+"_thb"+self.format
    
    
    
        command = ["ffmpeg","-i",self.i_path,"-vframes","1","-s",str(self.frame_size),"-v","-10","-y",o_path]
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
        self.frame_size = "vga"
        self.fps = 1



#/////////////// Interface Methods //////////////

    def UpdateConfig(self,config):
        self.format = config["format"]
        self.leading_zeros = config["zeros"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        
    

    def ExtractFrames(self):
#        get movie name    
        dot = self.i_path.find(".")
        mov_name = self.i_path[0:dot]
        o_path = self.o_path+mov_name+"%"+str(self.leading_zeros)+"d"+self.format
        
        command = ["ffmpeg","-i",self.i_path,"-vsync",str(self.fps),"-s",self.frame_size,"-v","-10","-y",o_path]
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
        
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]

    def Convert(self):
    
        for i_file in self.i_path:
    #        get movie name

            dot = i_file.find(".")
            mov_name = i_file[0:dot]
            o_path = self.o_path+mov_name+"_conv"+self.format
            

            command = ["ffmpeg","-i",i_file,"-s",self.frame_size,"-r",str(self.fps),o_path]
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
        self.frame_size = "vga"
        self.fps = 25
        
    def UpdateConfig(self,config):
        self.format = config["format"]
        self.i_path = config["i_path"]
        self.o_path = config["o_path"]
        self.frame_size = config["frame_size"]
        self.fps = config["fps"]
        self.leading_zeros = config["zeros"]
        

    def Stream(self):
#        get movie name    
        dot = self.i_path.find(".")

        i_format = self.i_path[(dot):(len(self.i_path))]
        i_name =  self.i_path[0:(dot-self.leading_zeros)]
        print i_format
        print i_name
        
        
        o_path = self.o_path+i_name+"_stream"+self.format
        
        i_path = i_name+"%"+str(self.leading_zeros)+"d"+i_format
        

        command = ["ffmpeg","-r",str(self.fps),"-i",i_path,"-s",self.frame_size,"-r",str(self.fps),o_path]
        subprocess.call(command)       
        
    
    
 








if __name__ == '__main__':



    i_path_list = list()
    i_path_list.append("test.mov")
    config={"format":".png","zeros":3,"i_path":"test.mov","o_path":"","frame_size":"vga","fps":1}
    config_c={"format":".mov","zeros":3,"i_path":i_path_list,"o_path":"","frame_size":"vga","fps":25}
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


