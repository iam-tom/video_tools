import os

from PIL import Image
import avtools

import utils
from threading import Thread
from waitbar import iWaitbar
from multiprocessing import Process
class tlm (Thread):



#    MEMBER VARIABLES
#   self.in_dir...... string ...... directory, containing input files
#       .in_files.... list(str) ... list with filenames
#       .out_dir .... string ...... directory for output
#       .ul_x ....... tuple(int) .. upper left corners of crop boxes x component
#       .ul_y .......   "        ..         "           "            y component
#       .dr_x .......   "        .. down right corners of crop boxes x component
#       .dr_y .......   "        ..         "           "            y component
#       .flags ...... dict       .. configuration flags

#   API - METHODS
#       TLM =  tlm()................ ....... constructor
#       T.SetIO() ..........................  Set input file list or input dir and output dir       
#       T.Seq2Seq(config) .................. tl from image sequence - output is image sequence
#       T.Seq2Vid(cinfig) .................. tl from image sequence - output is video
#       T.Vid2Seq(config) .................. tl from video - output is image sequence
#       T.Vid2Vid(config) .................. tl from video - output is video

    def __init__(self):
        Thread.__init__(self)
        Thread.__init__(self)
        self.deamon=True
        
        self.in_files = list()
        self.ul_x = tuple()
        self.ul_y = tuple()
        self.dr_x = tuple()
        self.dr_y = tuple()
#        default values for flags
        self.flags={"filter":Image.BICUBIC}
        print 114
        #self.pb = iWaitbar(None)
        print 115
#////////////NEW API//////

    def SetIO(self,in_path,out_path):
        if os.path.isdir(in_path[0]) == True:
            self.make_in_files()
            self.in_dir = in_path
        else:
            self.in_files = in_path
            slash = in_path[0].rfind("/")
            self.in_dir = in_path[0:slash]
            
        self.out_dir = out_path
        
        
        
#config ={"res":"","fps":"","box_start":"","box_end":""}
        
        
    def Seq2Seq(self,config):

#        update config
        self.frame_size=config["res"]
        self.fps=config["fps"]
        self.box0  =config["box_start"]
        self.box1  =config["box_end"]
        self.ul_0 =self.box0[0]
        self.dr_0=self.box0[1]        
        self.ul_1=self.box1[0]
        self.dr_1=self.box1[1]
        self.flag="Seq2Seq" 
        print "STARTING THREAD"
        self.start()
       # #        process
       # self.compute_boxes(self.in_files,ul_0,dr_0,ul_1,dr_1)
       # 
       # self.crop_scale_save(self.in_files,frame_size,self.out_dir)
        
        
        
        
    def Seq2Vid(self,config):
#        update config
        self.frame_size=config["res"]
        self.fps=config["fps"]
        self.box0  =config["box_start"]
        self.box1  =config["box_end"]

        self.ul_0 =self.box0[0]
        self.dr_0=self.box0[1]        
        self.ul_1=self.box1[0]
        self.dr_1=self.box1[1]            

        self.temp_path_crop = "/tmp/tlm_crops/"  
        self.flag="Seq2Vid"
        self.start()
##       self. process
#
#        self.flag="Seq2Vid" 
# 
#        self.compute_boxes(self.in_files,ul_0,dr_0,ul_1,dr_1)
#        self.crop_scale_save(self.in_files,frame_size,temp_path_crop)
#        self.stream(temp_path_crop,fps,self.out_dir)  
#
#        self.clean_temp(temp_path_crop)    
            
    def Vid2Seq(self,config):
#        update config       dr_1=config["box_end"][1]
        self.frame_size=config["res"]
        self.fps=config["fps"]
        self.box0  =config["box_start"]
        self.box1  =config["box_end"]
        self.ul_0 =self.box0[0]
        self.dr_0=self.box0[1]        
        self.ul_1=self.box1[0]
        self.dr_1=self.box1[1]             
        self.temp_path = "/tmp/tlm_frames/"
        self.flag="Vid2Seq"
        self.start()
##        process
#        if len(self.in_files) > 1:
#            print "to be implemented"
#            quit()
#        else:
#            self.extract_frames(fps,self.in_files,temp_path)
#            
#            tmp_files =  self.files_from_dir(temp_path)
#            self.compute_boxes(tmp_files,ul_0,dr_0,ul_1,dr_1)
#            self.crop_scale_save(tmp_files,frame_size,self.out_dir)  
#        
#        self.clean_temp(temp_path)
    def Vid2Vid(self,config):
#        update config
        self.frame_size=config["res"]
        self.fps=config["fps"]
        self.box0  =config["box_start"]
        self.box1  =config["box_end"]
        self.ul_0 =self.box0[0]
        self.dr_0=self.box0[1]        
        self.ul_1=self.box1[0]
        self.dr_1=self.box1[1]       
        self.temp_path_full = "/tmp/tlm_frames/"
        self.temp_path_crop = "/tmp/tlm_crops/"  
        self.flag="Vid2Vid"
        self.start()
##        process
#        if len(self.in_files) > 1:
#            print "to be implemented"
#            quit()
#        else:
#            self.extract_frames(fps,self.in_files,temp_path_full)
#            tmp_files =  self.files_from_dir(temp_path_full)
#            self.compute_boxes(tmp_files,ul_0,dr_0,ul_1,dr_1)
#            self.crop_scale_save(tmp_files,frame_size,temp_path_crop)
#            self.stream(temp_path_crop,fps,self.out_dir)   
#        self.clean_temp(temp_path_full)  
#        self.clean_temp(temp_path_crop)


#////////////////////////////////       
    def run(self):
        if  self.flag is "Vid2Vid":            
#           process
            if len(self.in_files) > 1:
                print "to be implemented"
                quit()
            else:
                #self.pb.Start()
                self.extract_frames(self.fps,self.in_files,self.temp_path_full)
                #self.pb.SetValue(30)
                tmp_files =  self.files_from_dir(self.temp_path_full)
                self.compute_boxes(tmp_files,self.ul_0,self.dr_0,self.ul_1,self.dr_1)
                self.crop_scale_save(tmp_files,self.frame_size,self.temp_path_crop)
                #self.pb.Increment(40)
                
                self.stream(self.temp_path_crop,self.fps,self.out_dir)   
                #self.pb.SetValue(90)
            self.clean_temp(self.temp_path_full)  
            self.clean_temp(self.temp_path_crop)
            #self.pb.Done() 
        if self.flag is "Seq2Seq": 
            #        process
            self.compute_boxes(self.in_files,self.ul_0,self.dr_0,self.ul_1,self.dr_1)
            
            self.crop_scale_save(self.in_files,self.frame_size,self.out_dir)
        
        
        if self.flag is "Vid2Seq":
#             process
             if len(self.in_files) > 1:
                 print "to be implemented"
                 quit()
             else:
                 self.extract_frames(self.fps,self.in_files,self.temp_path)
                 
                 tmp_files =  self.files_from_dir(self.temp_path)
                 self.compute_boxes(tmp_files,self.ul_0,self.dr_0,self.ul_1,self.dr_1)
                 self.crop_scale_save(tmp_files,self.frame_size,self.out_dir)  
             
             self.clean_temp(self.temp_path)
        if self.flag is "Seq2Vid": 
#           self. process

 
            self.compute_boxes(self.in_files,self.ul_0,self.dr_0,self.ul_1,self.dr_1)
            self.crop_scale_save(self.in_files,self.frame_size,self.temp_path_crop)
            self.stream(self.temp_path_crop,self.fps,self.out_dir)  

            self.clean_temp(self.temp_path_crop)    
#//////////internal methods////////////      

    def process_config(self,config,frame_size,fps,ul_0,dr_0,ul_1,dr_1): 
        frame_size=config["res"]
        fps=config["fps"]
        box0  =config["box_start"]
        box1  =config["box_end"]
        print box0 
        ul_0 =box0[0]
        dr_0=box0[1]        
        ul_1=box1[0]
        dr_1=box1[1]
    def frame_size_str(self,in_size):
        fs_str= str()
        fs_str+=str(in_size[0])
        fs_str+="x"
        fs_str+=str(in_size[1])
        return fs_str 

    def files_from_dir(self,path):
        file_list = list()
        allf = sorted(os.listdir(path)); 
        for i in xrange(len(allf)-1, -1, -1):
            if os.path.isdir(path+ os.path.sep + allf[i]):
                str_ =path+allf.pop(i)
                file_list.append(str_)
            else:
                str_ =path+allf.pop(i)
                file_list.append(str_)
        return file_list
               
    def extract_frames(self,fps,vid_file,out_path):
        fe = avtools.frame_extractor()
        fe_config={"format":".png","zeros":5,"i_path":vid_file,"o_path":out_path,"fps":fps,"frame_size":""}
        fe.UpdateConfig(fe_config)
        fe.Run()

  
    def set_flags(self,filter_method,mode):
        self.flags["filter"] = filter_method
  
    
    def make_in_files(self):
        allf = sorted(os.listdir(self.in_dir)); 
        for i in xrange(len(allf)-1, -1, -1):
            if os.path.isdir(self.in_dir[0] + os.path.sep + allf[i]):
                str_ =self.in_dir+allf.pop(i)
                self.in_files.append(str_)
            else:
                str_ =self.in_dir+allf.pop(i)
                self.in_files.append(str_)
                
                
    def stream(self,i_dir,fps,out_dir):
        config_s={"format":".mov","zeros":5,"i_path":i_dir,"o_path":out_dir,"fps":25}
        stream = avtools.streamer()
        stream.UpdateConfig(config_s)
        
        stream.Run()
                


    def clean_temp(self,path):
        cmd = "rm "+path+"*"
        os.system(cmd)      
   

#/////////old API//////////////        

    
    def compute_boxes(self,files,ul_0,dr_0,ul_1,dr_1):

        steps = len(files)
        range_x_ul = ul_1[0] - ul_0[0]
        range_y_ul = ul_1[1] - ul_0[1]
     
        range_x_dr = dr_1[0] - dr_0[0]
        range_y_dr = dr_1[1] - dr_0[1]        
        dx_ul= (range_x_ul / steps)
        dy_ul= (range_y_ul / steps)
            
        dx_dr= (range_x_dr / steps)
        dy_dr= (range_y_dr / steps)
            
                    
        step = 0
        while step <= steps:
            self.ul_x+= ul_0[0]+int(step*dx_ul),
            self.ul_y+= ul_0[1]+int(step*dy_ul),
            
            self.dr_x+= dr_0[0]+ int(step*dx_dr),
            self.dr_y+= dr_0[1]+ int(step*dy_dr),
            step += 1

        
    def crop_scale_save(self,files,o_size,o_path):
        
        utils.assert_dir(o_path)
        #chk = os.path.isdir(o_path)
        #if chk == False:
        #    cmd = "mkdir -p  "+o_path
        #    os.system("cmd")

        splitter=utils.split_seq(files,4)
        split_indices=splitter.get_indices()
        print split_indices
        p1=Process(target=self.css_parallel,args=(files[0:split_indices[1]]          ,o_size,o_path,0))
        p2=Process(target=self.css_parallel,args=(files[split_indices[1]:split_indices[3]],o_size,o_path,split_indices[1]))
        p3=Process(target=self.css_parallel,args=(files[split_indices[2]:split_indices[3]],o_size,o_path,split_indices[2]))
        p4=Process(target=self.css_parallel,args=(files[split_indices[3]:-1]          ,o_size,o_path,split_indices[3]))
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        
        p1.join()
        p2.join()
        p3.join()
        p4.join()
    
    def css_parallel(self,files,o_size,o_path,ctr):    
        i = ctr  
        in_bounds = i
               
        for curr_frame in files:


            img = Image.open(curr_frame)

            img_size = img.size
            if self.dr_x[i] < img_size[0] and self.dr_y[i] < img_size[1]:
                img = img.crop((self.ul_x[i],self.ul_y[i],self.dr_x[i],self.dr_y[i]))
                in_bounds = i
            else:
                img = img.crop((self.ul_x[in_bounds],self.ul_y[in_bounds],self.dr_x[in_bounds],self.dr_y[in_bounds]))
            img = img.resize(o_size,self.flags["filter"])
            number_str=utils.zero_str(5,i)
            o_file = o_path+"img_"+number_str+".jpg"
            img.save(o_file)
            i = i+1
#////////////////////////////////////




if __name__ == '__main__':



#    needed:
#    upper left corner of start frame
    start_corner=(500,0)
    end_corner = (1600,500)
#    frame_size = (1920,1080)
    frame_size = (50,50)
    output_size = (20,20)
    #in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/raw_lapses/lapse_0/"
    o = "/home/tom/lapse1"
    

    TLM = tlm(in_path,o)
    TLM.computeBoxes(start_corner,end_corner)
    TLM.crop_scale_save(frame_size,output_size)
    



