import sys
import os
import wx
import iwx
import cStringIO
from PIL import Image

from TimeLapseTools import tlm
from av_tools import thumbnailer
from av_tools import frame_extractor

# changed tlm api - maybe leads to errors
# changed to opitonal zoom mode maybe leads to errors

class tlmGUI(wx.Panel):
    def __init__(self, parent,config):
    
#//////////////// allocations /////////////////

        self.positions = list()
    
        self.in_path = list()
        self.size = config["size"]
        
        self.init_img = ".data/tlm_init.png"
        
        
        self.vid_mode = False # default is im_seq mode
#       self.vid_mode  = True # default is vid mode
        self.zoom_mode = False #default is pan only
#        self.zoom_mode = True #default is pan only
        
        
        
#//////////////// graphical elements /////////        
        p_size=(self.size[0],self.size[1])

        wx.Panel.__init__(self, parent,size=p_size)
#        button panel
        b_accept=wx.Button(self,wx.ID_OK,"OK",(0,(self.size[1]*4)/5),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,lambda  evt , config = config: self.OnAccept(evt,config))
        
#        b_browse =wx.TextCtrl(self, -1, "", pos=(100,(self.size[1]*4)/5))
        self.b_browse = iwx.iBrowse(self,(200,(self.size[1]*4)/5))
        
        choices_out_mode=["Img Sequence","Video"]
        self.choices_out_mode=wx.Choice(self, wx.ID_ANY, pos= (500,(self.size[1]*4)/5), size=(70,30), choices=choices_out_mode)
      

        
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
            
        
        
    def check_zoom_mode(self):
        self.zoom_mode = True
        print "to be implemented"     
        

    def get_out_dir(self):
        out_path = self.b_browse.GetData()
        slash = out_path.rfind("/")
        if (len(out_path)-slash) >1:
            out_path+="/"
        chk = os.path.isdir(out_path)
        if chk == False:
            self.make_dir(out_path)
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
            
    def OnAccept(self,e, config):
            out_path = self.get_out_dir()        
            T = tlm()
                 #config ={"res":"","fps":"","box_start":"","box_end":""}
            T.SetIO(self.in_path,out_path)
            box0=list()
            box1=list()
            box1.append((self.positions[2][0],self.positions[2][1]))
            box1.append((self.positions[3][0],self.positions[3][1]))
            box0.append((self.positions[0][0],self.positions[0][1]))
            box0.append((self.positions[1][0],self.positions[1][1]))
            config ={"res":(640,480),"fps":25,"box_start":box0,"box_end":box1}
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

        self.check_zoom_mode()
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
        elif len(self.positions) == 3 and self.zoom_mode == False:
            dim_box1=(self.positions[1][0]- self.positions[0][0],self.positions[1][1]- self.positions[0][1])
            ul = self.positions[2]
            dr = (self.positions[2][0]+dim_box1[0],self.positions[2][1]+dim_box1[1])
            self.positions.append(dr)
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("blue",style=wx.SOLID))
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
            
        elif len(self.positions) == 4 and self.zoom_mode == True:
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
        
        
        
class imgList (iwx.iList):
#iwx.iList with previer and type check
    def __init__(self,parent,i_size,i_pos):
        i_col_list = list()
        i_col_list.append("name")
        i_col_list.append("format")
        self.prev_config ={"pos":(i_size[0]+140,60),"parent":parent}
        
        super(imgList,self).__init__(parent,i_size,i_pos,i_col_list)
        b_prev=wx.Button(parent,wx.ID_ANY,"Preview",(i_size[0]+20,160),(70,30),wx.BU_EXACTFIT)
        b_prev.Bind(wx.EVT_BUTTON, self.OnPrev,b_prev)
        self.T = thumbnailer()
        self.prev_init_state()
        wx.StaticText(parent,wx.ID_ANY,"Preview",pos=(i_size[0]+140,40))	

        

        
    def prev_init_state(self):
        self.config = {"format":".png","frame_size":"qvga", "i_path":"", "o_path":"/tmp/" }

        bmp  = self.get_bmp(".data/prev_init.png")
        self.canvas =wx.StaticBitmap(self.prev_config["parent"], -1, bmp,self.prev_config["pos"] )    

    def get_bmp(self,path):
        data = open(path, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        image = wx.ImageFromStream( stream )  

        bmp = wx.BitmapFromImage(image)
        return bmp
                
    def OnPrev(self,e):
        
        index = self.get_selected()
        self.config["i_path"] = self.path_list[index[0]]
        
        self.T.UpdateConfig(self.config)
        self.T.Run()
        
        bmp = self.get_bmp("/tmp/thb"+self.config["format"])
       
        self.canvas.SetBitmap( bmp)
        
    def OnReset(self,e):
        iwx.iList.OnReset(self,e)
        self.prev_init_state()
        
              



