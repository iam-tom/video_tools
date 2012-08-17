import os

from PIL import Image
import av_tools


class tlm (object):



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
        self.in_files = list()
        self.ul_x = tuple()
        self.ul_y = tuple()
        self.dr_x = tuple()
        self.dr_y = tuple()
#        default values for flags
        self.flags={"filter":Image.BICUBIC}
        

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
        frame_size=config["res"]
        fps=config["fps"]
        box0  =config["box_start"]
        box1  =config["box_end"]
        ul_0 =box0[0]
        dr_0=box0[1]        
        ul_1=box1[0]
        dr_1=box1[1]
        
        #        process
        self.compute_boxes(self.in_files,ul_0,dr_0,ul_1,dr_1)
        
        self.crop_scale_save(self.in_files,frame_size,self.out_dir)
        
        
        
        
    def Seq2Vid(self,config):
#        update config
        frame_size=config["res"]
        fps=config["fps"]
        box0  =config["box_start"]
        box1  =config["box_end"]

        ul_0 =box0[0]
        dr_0=box0[1]        
        ul_1=box1[0]
        dr_1=box1[1]            

        temp_path_crop = "/tmp/tlm/crops/"  
#        process
        if len(self.in_files) > 1:
            print "to be implemented"
            quit()
        else:
            self.compute_boxes(self.in_files,ul_0,dr_0,ul_1,dr_1)
            self.crop_scale_save(self.in_files,frame_size,temp_path_crop)
            self.stream(temp_path_crop,fps,self.o_dir)  
            
            
    def Vid2Seq(self,config):
#        update config       dr_1=config["box_end"][1]
        frame_size=config["res"]
        fps=config["fps"]
        box0  =config["box_start"]
        box1  =config["box_end"]
        ul_0 =box0[0]
        dr_0=box0[1]        
        ul_1=box1[0]
        dr_1=box1[1]             
        temp_path = "/tmp/tlm/frames/"
        
#        process
        if len(self.in_files) > 1:
            print "to be implemented"
            quit()
        else:
            self.extract_frames(self.in_files,temp_path)
            tmp_files =  self.files_from_dir(temp_path)
            self.compute_boxes(tmp_files,ul_0,dr_0,ul_1,dr_1)
            self.crop_scale_save(tmp_files,frame_size,self.out_dir)  
        
            

    def Vid2Vid(self,config):
#        update config
        frame_size=config["res"]
        fps=config["fps"]
        box0  =config["box_start"]
        box1  =config["box_end"]
        ul_0 =box0[0]
        dr_0=box0[1]        
        ul_1=box1[0]
        dr_1=box1[1]       
        temp_path_full = "/tmp/tlm/frames/"
        temp_path_crop = "/tmp/tlm/crops/"  
#        process
        if len(self.in_files) > 1:
            print "to be implemented"
            quit()
        else:
            self.extract_frames(self.in_files,temp_path_full)
            tmp_files =  self.files_from_dir(temp_path_full)
            self.compute_boxes(tmp_files,ul_0,dr_0,ul_1,dr_1)
            self.crop_scale_save(tmp_files,frame_size,temp_path_crop)
            self.stream(temp_path_crop,fps,self.o_dir)   
   
  

#////////////////////////////////       
            
 
 
 
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
        fe = av_tools.frame_extractor()
        fe_config={"format":".png","zeros":4,"i_path":vid_file,"o_path":out_path,"fps":fps}
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
                
                
    def stream(self,i_dir,fps,o_dir):
        config_s={"format":".mov","zeros":4,"i_path":i_dir,"o_path":o_dir,"fps":25}
        stream = av_tools.streamer()
        stream.UpdateConfig(config_s)
        print self.out_dir
        stream.Run()
                


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
        i = 0  
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
            o_file = o_path+"/img_"+str(i)+".jpg"
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
    



