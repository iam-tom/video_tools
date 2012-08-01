import os
import wx
import wdManager
import subprocess



import iwx
from PIL import Image
import math

class tlm (object):

    def __init__(self,in_path,out_path):
        self.ul_x = tuple()
        self.ul_y = tuple()

    

    
    def computeFrames(self,ul_0,ul_1,steps):

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

        
    def process(self):
        i = 0
        box_size=(50,50)


        #while (u_l[0]+box_size[0]) <u_l_ff[0] and (u_l[1]+box_size[1] < u_l_ff[1]): 
        for p in self.ul_x:           
            #img2 = img.crop((u_l[0],u_l[1],box_size[0],box_size[1]))
            #img2 = img.crop((frame,200,frame+box_size[0],200+box_size[1]))
            img = Image.open("/home/tom/Pictures/Lebron-james_streetclothes.jpg")
            img2 = img.crop((self.ul_x[i],self.ul_y[i],self.ul_x[i]+box_size[0],self.ul_y[i]+box_size[1]))
            o_path = "/home/tom/lapse0/img_"+str(i)+".jpg"
            img2.save(o_path)
            i = i+1
            #print (p,0,p+100,200)
            #raw_input("press enter to continue")
            


if __name__ == '__main__':

    i = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0"
    o = "/home/tom/lapse0"
    TLM = tlm(i,o)
    TLM.computeFrames((0,0),(100,100),100)
    TLM.process()
    


