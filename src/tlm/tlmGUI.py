## @package TLM GUI
#
# The GUI frontend for the tlm module
import sys
import os
import wx
import iwx
import cStringIO
from PIL import Image
from tlm import tlm
from avtools import thumbnailer
from avtools import frame_extractor
import imgutils
import time
import utils
import GUIelements



## The class tlmGUI
class tlmGUI(wx.Panel):

# Member Variables:
# positions ..................... corner points of crop boxes
# canvas scale .................. scale factor from original img to canvas coordinates
# full size ..................... size of original image
# init_img ...................... initial image, displayed on canvas

    ##    
    #Init Function of GUI
    # @param self Object pointer
    # @param parent Parent Object
    # @param config Parameter Configuration    
    def __init__(self, parent):
        self.positions = list()
        self.in_path = list()
       
        self.full_size=tuple()
        self.canvas_scale=float()
       # #test configuration
       # self.init_img = "../../src/.data/tlm_init.png"
        self.init_img = ".data/tlm_init.png"
        
        
        self.vid_mode = False # default is im_seq mode
#       self.vid_mode  = True # default is vid mode


#---tl_modes:
#    1 - pan only default
#    2 - pan&zoom
#    3 - full
#    4 - 16/10 (1280x720)
        tl_mode = 1
#        self.zoom_mode = False #default is pan only
#        self.zoom_mode = True #default is pan only
#        sel.full_mode  = True #default is pan only        



        self.make_layout(parent)
        self.set_init_state()      
        self.make_bindings()

    ##
    # Establish graphical elements
    def make_layout(self,parent):
     
        size_canvas=wx.Size(900,600)

        # init wx panel
        wx.Panel.__init__(self, parent)
        

        # init sizers
        fgs0=wx.FlexGridSizer(rows=3,cols=1)
        bs0 = wx.BoxSizer(wx.HORIZONTAL)
        bs1 = wx.BoxSizer(wx.HORIZONTAL)
        bs2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # canvas element
        self.canvas=iwx.iCanvas(self,size_canvas)

        # button panel for output options
        # TODO: MAKE iChoice position independent
        # TODO: do i really want to use this?
        self.choices_res=GUIelements.iChoice(self,"res")
        self.choices_fps=GUIelements.iChoice(self,"fps")
        choices_out_mode=["Img Sequence","Video"]
        self.choices_out_mode_lookup=["1","2"]
        self.choices_out_mode=wx.Choice(self, wx.ID_ANY, size=(130,30), choices=choices_out_mode)

        # put elements in box sizer
        bs0.Add(self.choices_res)
        bs0.Add(self.choices_fps)
        bs0.Add(self.choices_out_mode)


        # button panel for process options
        choices_tl_mode=["Pan Only","Zoom&Pan","Full Image","16:9"]
        self.choices_tl_mode_lookup=[1,2,3,4]
        self.choices_tl_mode=wx.Choice(self, wx.ID_ANY,size=(130,30), choices=choices_tl_mode)
        self.b_reset = wx.Button(self,-1,"Reset")
        
        # put element in box sizer
        bs1.Add(self.choices_tl_mode)
        bs1.Add(self.b_reset)

        # button panel for path 
        self.b_accept=wx.Button(self,-1,"OK")
        self.b_browse = GUIelements.iBrowse(self)
        

        # put elements in box sizer
        bs2.Add(self.b_browse)
        bs2.Add(self.b_accept)


        # put elements to top level sizer
       # fgs0.AddGrowableRow(0,0)
        fgs0.Add(self.canvas)
        fgs0.Add(bs0)
        fgs0.Add(bs1)
        fgs0.Add(bs2)

        # make layout
        self.SetSizer(fgs0)
        self.Layout()
        self.Fit()


    def make_bindings(self):
        self.b_accept.Bind(wx.EVT_BUTTON, self.OnAccept)
        self.canvas.Bind(iwx.EVT_POS_sub,self.OnLeftClick)
        self.b_reset.Bind(wx.EVT_BUTTON,self.OnReset)            

       
        #self.choices_resolution_lookup=[self.full_size,(1280,720),(1920,1080),(640,480)]
        #choices_resolution=["Original","1280x720","1920x1080","640x480"] 
        #self.choices_resolution=wx.Choice(self,wx.ID_ANY,pos=(500,(self.size[1]*4)/5),size=(150,30),choices=choices_resolution)

        #choices_fps=["24fps","25fps","50fps"]
        #self. choices_fps_lookup=[24,25,50]
        #self.choices_fps=wx.Choice(self, wx.ID_ANY, pos= (700,((self.size[1]*4)/5)), size=(130,30), choices=choices_fps)
 
 
#///////////CALLBACKS /////////////

    def SetInPath(self,msg):
        self.in_path = msg[0]
        self.check_in_mode(self.in_path[0])
                        
        if self.vid_mode == False:
            self.set_state(msg[0][0])
        elif self.vid_mode == True:
            self.get_thumb(self.in_path[0])

            self.set_state("/tmp/imgGUI/thb.png")


    ##  @brief Generate Thumbnail of Video file
    def get_thumb(self,in_path):
        config = {"format":".png","frame_size":"", "i_path":in_path, "o_path":"/tmp/imgGUI/" }
        t = thumbnailer()
        t.UpdateConfig(config)
        t.Run()
            

            

        
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

        
        
    def check_tl_mode(self):
        chk = self.choices_tl_mode.GetCurrentSelection()
        if chk == 0:
            tl_mode=self.choices_tl_mode_lookup[0]
        elif chk ==1:
            tl_mode=self.choices_tl_mode_lookup[1]
        elif chk ==2:
            tl_mode=self.choices_tl_mode_lookup[2]
        elif chk ==3:
            tl_mode=self.choices_tl_mode_lookup[3]
        print "selection mode is %d"%tl_mode     
        return tl_mode 
    def check_fps(self):
        fps=self.choices_fps.GetChoice()
#        chk = self.choices_fps.GetCurrentSelection()
#        if chk == 0:
#            fps=self.choices_fps_lookup[0]
#        elif chk ==1:
#            fps=self.choices_fps_lookup[1]
#            
#        elif chk ==2:
#            fps=self.choices_fps_lookup[2]
#            
#        print "output fps is set to %i"%fps     
#
        return fps

    def check_resolution(self):
        res = self.choices_resolution.GetChoice()
      #  chk = self.choices_resolution.GetCurrentSelection()
      #  if chk ==0:
      #     res=self.choices_resolution_lookup[0]
      #     res=self.full_size
      #     
      #  elif chk ==1:
      #     res=self.choices_resolution_lookup[1]

      #  elif chk ==2:
      #     res=self.choices_resolution_lookup[2]

      #  elif chk ==3:
      #     res=self.choices_resolution_lookup[3]
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

    ##
    # @brief Set GUI to state
    #
    # @param[in] imageFile Path to image file
    def set_state(self,imageFile):   
        self.img=iwx.iFrame(imageFile)
        self.canvas.draw(self.img.img())
        self.make_bindings()
        

    ##
    # @brief Set GUI to initial state
    def set_init_state(self):
        # TODO: make id -1 default value for frame
        self.img=iwx.iFrame(self.init_img)
        self.canvas.draw(self.img.img())
    

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
            
##
# @brief Start processing
    def OnAccept(self,e):
            tl_mode = self.check_tl_mode() 
            if tl_mode ==3: # for mode with full frame
                self.positions[:]=[]
                self.positions.append((0,0))
                self.positions.append(self.img.size())
                self.positions.append((0,0))
                self.positions.append(self.img.size())
            
            out_path = self.get_out_dir()
            utils.assert_dir(out_path)        

            # init tlm
            T = tlm()
            T.SetIO(self.in_path,out_path)

            box0=list()
            box1=list()
            box1.append((self.positions[2][0],(self.positions[2][1])))
            box1.append((self.positions[3][0],(self.positions[3][1])))
            box0.append((self.positions[0][0],(self.positions[0][1])))
            box0.append((self.positions[1][0],(self.positions[1][1])))

            output_res = self.choices_res.GetChoice()
            output_fps = self.check_fps()
            seq_out = True 
            seq_out = self.check_out_mode()
            config ={"res":output_res,"fps":output_fps,"box_start":box0,"box_end":box1}
                
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


    ##
    # @brief Callback for left click on canvas
    # @detail Method handles clicked positions, draws on canvas
    # and saves clicked position
    def OnLeftClick(self, e):

        pos = e.GetVal()

        tl_mode = self.check_tl_mode()
        dc = wx.MemoryDC() 
        bitmap = wx.BitmapFromImage(self.img.img())
        dc.SelectObject(bitmap)

        self.positions.append(pos)
        if len(self.positions ) ==2 and tl_mode == 4:
            ul = self.positions[0]
            temp= self.positions[1]
            x_margin=self.positions[1][0]-self.positions[0][0]
            y_offset=int((float(x_margin)/16) *9)
            dr = wx.Point(x=self.positions[1][0],y=self.positions[0][1]+y_offset)
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("red",style=wx.SOLID))
            dc.SetBrush(wx.Brush("red", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
            self.positions[-1]=dr
        

        elif len(self.positions) == 2:
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

        elif len(self.positions ) ==4 and tl_mode == 4:
            ul = self.positions[2]
            x_margin=self.positions[3][0]-self.positions[2][0]
            y_offset=int((float(x_margin)/16) *9)
            dr = wx.Point(x=self.positions[3][0],y=self.positions[2][1]+y_offset)
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("blue",style=wx.SOLID))
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
            self.positions[-1]=dr

        image=wx.ImageFromBitmap(bitmap)
#TODO: make this more cleanly - no acces to member variable
        self.img.img_work_=image
        self.canvas.draw(self.img.img())
        
    ##
    # @brief Reset GUI and configuration
    def OnReset(self,e):
        self.img.reset()

        self.canvas.draw(self.img.img())
        self.positions[:] =[]
        
        
        
