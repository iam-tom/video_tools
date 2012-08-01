import os
import wx
import wdManager



import iwx
from PIL import Image

class tlm (object):

    def __init__(self,in_path,out_path):
        

    
        img = Image.open("/home/tom/Pictures/Lebron-james_streetclothes.jpg")
        
    def crop()
        i = 0
        box_size=(50,50)

        u_l_y= (0,0,0,0,0)
        u_l_x = (0,30,40,60,90)
        #while (u_l[0]+box_size[0]) <u_l_ff[0] and (u_l[1]+box_size[1] < u_l_ff[1]): 
        for p in u_l_x:           
            #img2 = img.crop((u_l[0],u_l[1],box_size[0],box_size[1]))
            #img2 = img.crop((frame,200,frame+box_size[0],200+box_size[1]))
            img2 = img.crop((u_l_x[i],u_l_y[i],u_l_x[i]+box_size[0],u_l_y[i]+box_size[1]))
            o_path = "/home/tom/lapse0/img_"+str(i)+".jpg"
            img2.save(o_path)
            i = i+1
            print (p,0,p+100,200)
            raw_input("press enter to continue")
            


if __name__ == '__main__':

    i = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0"
    o = "/home/tom/lapse0"
    TLM = tlm(i,o)
    TLM = crop()
    


