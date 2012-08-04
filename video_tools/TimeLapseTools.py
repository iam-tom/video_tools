import os

from PIL import Image


class tlm (object):

    def __init__(self,in_path,out_path):
        self.in_frames = list()
        self.in_path = in_path
        self.out_path = out_path
        self.ul_x = tuple()
        self.ul_y = tuple()
#        default values for flags
        self.flags={"filter":Image.BICUBIC}
        
        self.make_input_list()

        
    def set_flags(self,filter_method):
        self.flags["filter"] = filter_method
    
    def make_input_list(self):
        allf = sorted(os.listdir(self.in_path)); 
        for i in xrange(len(allf)-1, -1, -1):
            if os.path.isdir(self.in_path + os.path.sep + allf[i]):
               self.in_frames.append(allf.pop(i))
        self.in_frames.extend(allf) 
        

    
    def computeBoxes(self,ul_0,ul_1):
        steps = len(self.in_frames)
        range_x = ul_1[0] - ul_0[0]
        range_y = ul_1[1] - ul_0[1]
        if steps> range_x  and steps > range_y:
            print "warning: more steps, than pixel range"
            quit()
        else:
            dx= (range_x / steps)
            dy= (range_y / steps) 
                    
        step = 0
        while step <= steps:
            self.ul_x+= ul_0[0]+int(step*dx),
            self.ul_y+= ul_0[1]+int(step*dy),

            step += 1

        
    def crop_scale_save(self,box_size,o_size):
        i = 0
        


        for curr_frame in self.in_frames:           
            curr_str = self.in_path+curr_frame
            img = Image.open(curr_str)
            img_size = img.size
            if self.ul_x[i]+box_size[0] < img_size[0] and self.ul_y[i]+box_size[1]:
                img = img.crop((self.ul_x[i],self.ul_y[i],self.ul_x[i]+box_size[0],self.ul_y[i]+box_size[1]))
            else:
                img = img.crop((img_size[0]-box_size[0],img_size[1]-box_size[1],img_size[0],img_size[1]))
            img = img.resize(o_size,self.flags["filter"])
            o_path = self.out_path+"/img_"+str(i)+".jpg"
            img.save(o_path)
            i = i+1
            #print (p,0,p+100,200)
            #raw_input("press enter to continue")
            


if __name__ == '__main__':



#    needed:
#    upper left corner of start frame
    start_corner=(500,0)
    end_corner = (1600,500)
#    frame_size = (1920,1080)
    frame_size = (50,50)
    output_size = (20,20)
    in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/raw_lapses/lapse_0/"
    o = "/home/tom/lapse1"
    

    TLM = tlm(in_path,o)
    TLM.computeBoxes(start_corner,end_corner)
    TLM.crop_scale_save(frame_size,output_size)
    


