import sys


import os
import wx
import iwx
import cStringIO
from PIL import Image

from TimeLapseTools import tlm
from av_tools import thumbnailer
from av_tools import frame_extractor

import imgutils
import time

import utils

import GUIelements




class tlmGUI(wx.Panel):

# Member Variables:
# positions ..................... corner points of crop boxes
# canvas scale .................. scale factor from original img to canvas coordinates
# full size ..................... size of original image
# init_img ...................... initial image, displayed on canvas


    def __init__(self, parent,config):
    
#//////////////// allocations /////////////////

        self.positions = list()
    
        self.in_path = list()
        self.size = config["size"]
        self.full_size=tuple()
        
        self.canvas_scale=float()
        self.init_img = ".data/tlm_init.png"
        
        
        self.vid_mode = False # default is im_seq mode
#       self.vid_mode  = True # default is vid mode


#---tl_modes:
#    1 - pan only default
#    2 - pan&zoom
#    3 - full
        tl_mode = 1
#        self.zoom_mode = False #default is pan only
#        self.zoom_mode = True #default is pan only
#        sel.full_mode  = True #default is pan only        
        
        
#//////////////// graphical elements /////////        
        p_size=(self.size[0],self.size[1])

        wx.Panel.__init__(self, parent,size=p_size)
#        button panel
        b_accept=wx.Button(self,wx.ID_OK,"OK",(0,(self.size[1]*4)/5),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,lambda  evt , config = config: self.OnAccept(evt,config))
        
#        b_browse =wx.TextCtrl(self, -1, "", pos=(100,(self.size[1]*4)/5))
        self.b_browse = GUIelements.iBrowse(self,(100,(self.size[1]*4)/5))
        
        choices_out_mode=["Img Sequence","Video"]
        self.choices_out_mode_lookup=["1","2"]
        self.choices_out_mode=wx.Choice(self, wx.ID_ANY, pos= (350,(self.size[1]*4)/5), size=(130,30), choices=choices_out_mode)
      

        choices_tl_mode=["Pan Only","Zoom&Pan","Full Image"]
        self.choices_tl_mode_lookup=[1,2,3]
        self.choices_tl_mode=wx.Choice(self, wx.ID_ANY, pos= (700,((self.size[1]*4)/5)-50), size=(130,30), choices=choices_tl_mode)
       
        #self.choices_resolution_lookup=[self.full_size,(1280,720),(1920,1080),(640,480)]
        #choices_resolution=["Original","1280x720","1920x1080","640x480"] 
        #self.choices_resolution=wx.Choice(self,wx.ID_ANY,pos=(500,(self.size[1]*4)/5),size=(150,30),choices=choices_resolution)

        self.choices_res=GUIelements.iChoice(self,(500,(self.size[1]*4)/5),"res")
        self.choices_fps=GUIelements.iChoice(self, (700,(self.size[1]*4)/5),"fps")
        #choices_fps=["24fps","25fps","50fps"]
        #self. choices_fps_lookup=[24,25,50]
        #self.choices_fps=wx.Choice(self, wx.ID_ANY, pos= (700,((self.size[1]*4)/5)), size=(130,30), choices=choices_fps)
        self.setInitState()      


        
        
#//////////////// PUBSUB /////////
 

 
 
 
 
 
#///////////CALLBACKS /////////////

    def SetInPath(self,msg):
        self.in_path = msg[0]
        self.check_in_mode(self.in_path[0])
                        
        if self.vid_mode == False:
            self.setNewState(msg[0][0])
        elif self.vid_mode == True:
            self.get_thumb(self.in_path[0])

            self.setNewState("/tmp/imgGUI/thb.png")

            

        
    def check_out_mode(self):
        chk =self.choices_out_mode.GetCurrentSelection()
        
        if chk == 0:
            seq_out = True
        elif chk ==1:
            seq_out = False
        return seq_out
                        
    def check_in_mode(self,i_file):
        
        formats={".avi",".AVI",".mov",".MOV",".mp4",".mpeg"}
        
        dot =i_file.rfind(".")
        suffix =i_file[dot:len(i_file)]
        chk = suffix in formats
        if chk == True:
            self.vid_mode = True			

    def get_thumb(self,in_path):
        config = {"format":".png","frame_size":"", "i_path":in_path, "o_path":"/tmp/imgGUI/" }
        t = thumbnailer()
        t.UpdateConfig(config)
        t.Run()
            
        
        
    def check_tl_mode(self):
        chk = self.choices_tl_mode.GetCurrentSelection()
        if chk == 0:
            tl_mode=self.choices_tl_mode_lookup[0]
        elif chk ==1:
            tl_mode=self.choices_tl_mode_lookup[1]
        elif chk ==2:
            tl_mode=self.choices_tl_mode_lookup[2]
        print "selection mode is %d"%tl_mode     
        return tl_mode 
    def check_fps(self):
        chk = self.choices_fps.GetCurrentSelection()
        if chk == 0:
            fps=self.choices_fps_lookup[0]
        elif chk ==1:
            fps=self.choices_fps_lookup[1]
            
        elif chk ==2:
            fps=self.choices_fps_lookup[2]
            
        print "output fps is set to %i"%fps     

        return fps

    def check_resolution(self):
        
        chk = self.choices_resolution.GetCurrentSelection()
        if chk ==0:
           res=self.choices_resolution_lookup[0]
           res=self.full_size
           
        elif chk ==1:
           es=self.choices_resolution_lookup[1]

        elif chk ==2:
           res=self.choices_resolution_lookup[2]

        elif chk ==3:
           res=self.choices_resolution_lookup[3]
        return res

    def get_out_dir(self):
        out_path = self.b_browse.GetData()
        utils.assert_dir(out_path)
        slash = out_path.rfind("/")
        if (len(out_path)-slash) >1:
            out_path+="/"

       # chk = os.path.isdir(out_path)
       # if chk == False:
       #     self.make_dir(out_path)
        return out_path
    
    def make_dir(self,path):
        cmd = "mkdir "+path
        os.system(cmd)
        
    def setNewState(self,imageFile):   
    
    
        
#     wipe canvas   
            
            

    #        CLEAN VERISION

            data_orig = open(imageFile, "rb").read()
            # convert to a data stream
            stream_orig = cStringIO.StringIO(data_orig)
            # convert to a bitmap
            image =  wx.ImageFromStream( stream_orig )
            self.full_size=image.GetSize()
            self.set_canvas_scale(image)
            image = self.scale_image(image)
            self.bmp_orig = wx.BitmapFromImage(image)

            
    #        PULLUTE VERSION
            data = open(imageFile, "rb").read()
            # convert to a data stream
            stream = cStringIO.StringIO(data)
            # convert to a bitmap
            image = wx.ImageFromStream( stream )
            image = self.scale_image(image)

            self.bmp_work = wx.BitmapFromImage(image) 
            # show the bitmap, (5, 5) are upper left corner coordinates
            #self.canvas =wx.StaticBitmap(self, -1, bmp, (0, 0))
            self.canvas.SetBitmap(self.bmp_work)
            self.canvas.Bind(wx.EVT_LEFT_DOWN,self.OnLeftClick)
            self.canvas.Bind(wx.EVT_RIGHT_DOWN,self.OnRightClick)            

        

       
    def setInitState(self):
        imageFile = self.init_img    
        

        
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        image = wx.ImageFromStream( stream )
        image = self.scale_image(image)

        

        bmp = wx.BitmapFromImage(image)

        self.canvas =wx.StaticBitmap(self, -1, bmp, (0, 0))
    
    def scale_image(self,image):
        o_width = image.GetWidth()
        o_height = image.GetHeight()

        q = float(self.size[0]) /float( o_width)
        new_width = self.size[0]
        new_height = o_height*q
        
        if new_height*5 > self.size[1]*4:
            print "rescaling"
            new_height = (self.size[1]*4)/5

            q = float(new_height)/float(o_height)
            new_width = o_width *q
            
#        if new_width >  o_width:
#            new_width =  o_width
#            q = float(new_width) /float( o_width)
#            new_height = o_height  * q
#        elif new_height > o_height:
        
#            new_height = o_height
#            q =float(new_height) /float( o_height)
#            new_height = o_height  * q

        
       
        image = image.Scale(new_width,new_height,wx.IMAGE_QUALITY_HIGH)
        return image
        
    def set_canvas_scale(self,image):
        o_width = image.GetWidth()
        o_height = image.GetHeight()

        q = float(self.size[0]) /float( o_width)
        new_width = self.size[0]
        new_height = o_height*q
        
        if new_height*5 > self.size[1]*4:

            new_height = (self.size[1]*4)/5
            q = float(new_height)/float(o_height)
        self.canvas_scale=q   
            
    def OnAccept(self,e, config):
            tl_mode = self.check_tl_mode() 
            if tl_mode ==3:
                self.positions[:]=[]
                self.positions.append((0,0))
                self.positions.append(self.full_size)
                self.positions.append((0,0))
                self.positions.append(self.full_size)
            else:
                l=list()
                for point in self.positions:
                    x=point[0] / self.canvas_scale
                    y=point[1] / self.canvas_scale 
                    t=(int(x),int(y))
                    l.append(t)
                self.positions=l 
            
            out_path = self.get_out_dir()
            utils.assert_dir(out_path)        
            T = tlm()
            #config ={"res":"","fps":"","box_start":"","box_end":""}
            T.SetIO(self.in_path,out_path)
            box0=list()
            box1=list()
            box1.append((self.positions[2][0],(self.positions[2][1])))
            box1.append((self.positions[3][0],(self.positions[3][1])))
            box0.append((self.positions[0][0],(self.positions[0][1])))
            box0.append((self.positions[1][0],(self.positions[1][1])))

            #output_res = self.check_resolution()
            output_res = self.choices_res.GetChoice()
            output_fps = self.check_fps()

            config ={"res":output_res,"fps":output_fps,"box_start":box0,"box_end":box1}
            seq_out = True 
            seq_out = self.check_out_mode()
                
            if self.vid_mode ==True:
                if seq_out ==True:
                    print"VID2SEQ"
                    T.Vid2Seq(config)
                else:
                   print"VID2VID"
                   T.Vid2Vid(config)

            if self.vid_mode ==False:
                if seq_out ==True:
                    print"SEQ2SEQ"
                    T.Seq2Seq(config)
                else:
                    print"SEQ2VID"
                    T.Seq2Vid(config)               
                
            print "DONE"    


    def OnLeftClick(self, e):

        tl_mode = self.check_tl_mode()
        pos = e.GetPosition()
        dc = wx.MemoryDC() 
        dc.SelectObject(self.bmp_work)
        self.positions.append(pos)
        if len(self.positions) == 2:
            ul = self.positions[0]
            dr = self.positions[1]
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("red",style=wx.SOLID))
            dc.SetBrush(wx.Brush("red", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
        elif len(self.positions) == 3 and tl_mode == 1:
            dim_box1=(self.positions[1][0]- self.positions[0][0],self.positions[1][1]- self.positions[0][1])
            ul = self.positions[2]
            dr = wx.Point(x=self.positions[2][0]+dim_box1[0],y=self.positions[2][1]+dim_box1[1])
            self.positions.append(dr)
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("blue",style=wx.SOLID))
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
            
        elif len(self.positions) == 4 and tl_mode == 2:
            ul = self.positions[2]
            dr = self.positions[3]
            dc.SetPen(wx.Pen("blue",style=wx.SOLID))
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()

        self.canvas.SetBitmap(self.bmp_work)
        
    def OnRightClick(self, e):


#        wx.StaticBitmap(self, -1, self.bmp_orig)
#        reset PULLUTE VERSION to CLEAN VERSION
        self.canvas.SetBitmap(self.bmp_orig)
        self.positions[:] =[]
        self.bmp_work = self.bmp_orig
        print "reset"
        
        
        
    def OnAdd(self,e):
        dlg = wx.FileDialog(None,"Choose Files ",style =wx.FD_MULTIPLE )
        if dlg.ShowModal() == wx.ID_OK:
            new_files = dlg.GetFilenames()
            new_paths = dlg.GetPaths()
            
            self.path_list = new_paths
            self.file_list =  new_files
            self.disp_list = new_files
        dlg.Destroy()
# When Sequence Detection is active
        if self.chkbx.IsChecked()==True:

            sc = imgutils.seq_compressor(set(self.path_list))
            groups= sc.get_groups()
            self.file_mapping=sc.get_mapping()
           
            meta = sc.get_meta()
            self.disp_list = list(groups)
            print self.disp_list
            i=0
            for f in self.disp_list:
                print "format = %s"% meta[i]["format"]
                self.LC.InsertStringItem(0,f)    
                self.LC.SetStringItem(0,1,meta[i]["format"])  
                i=i+1
        else:
            for f in self.disp_list:

                self.LC.InsertStringItem(0,f)
                
        
