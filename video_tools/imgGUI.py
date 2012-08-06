import sys
import wx
import cStringIO
from PIL import Image
from wx.lib.pubsub import Publisher


class GUI(wx.Panel):
    def __init__(self, parent,config):
    
#//////////////// allocations /////////////////

        self.positions = list()
    
        self.in_path = config["i_file"]
        self.size = config["size"]
        
        self.init_img = ".data/tlm_init.png"
        
#//////////////// graphical elements /////////        
        p_size=(self.size[0],self.size[1]+30)

        wx.Panel.__init__(self, parent,size=p_size)
#        button panel
        b_accept=wx.Button(self,wx.ID_OK,"OK",(0,self.size[1]),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,lambda  evt , config = config: self.OnAccept(evt,config))

        
        
        self.setInitState()        

    def setNewState(self,in_path):
        
#     wipe canvas   
            
            

    #        CLEAN VERISION
            imageFile = in_path
            data_orig = open(imageFile, "rb").read()
            # convert to a data stream
            stream_orig = cStringIO.StringIO(data_orig)
            # convert to a bitmap
            self.bmp_orig = wx.BitmapFromImage( wx.ImageFromStream( stream_orig ))
            
    #        PULLUTE VERSION
            data = open(imageFile, "rb").read()
            # convert to a data stream
            stream = cStringIO.StringIO(data)
            # convert to a bitmap
            bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
            # show the bitmap, (5, 5) are upper left corner coordinates
           #self.canvas =wx.StaticBitmap(self, -1, bmp, (0, 0))
            self.canvas.SetBitmap(bmp)
            self.canvas.Bind(wx.EVT_LEFT_DOWN,self.OnLeftClick)
            self.canvas.Bind(wx.EVT_RIGHT_DOWN,self.OnRightClick)            

        

       
    def setInitState(self):
        imageFile = self.init_img    
        

        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        self.canvas =wx.StaticBitmap(self, -1, bmp, (0, 0))
    
        
    def OnAccept(self,e, config):
   
        Publisher().sendMessage(("imgGUI.positions"), self.positions)    


    def OnLeftClick(self, e):


        pos = e.GetPosition()
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        self.positions.append(pos)
        
        if len(self.positions) == 2:
            ul = self.positions[0]
            dr = self.positions[1]
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("red",style=wx.SOLID))
            dc.SetBrush(wx.Brush("red", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()
        elif len(self.positions) == 4:
            ul = self.positions[2]
            dr = self.positions[3]
            dc.BeginDrawing()
            dc.SetPen(wx.Pen("blue",style=wx.SOLID))
            dc.SetBrush(wx.Brush("blue", wx.TRANSPARENT))
            dc.DrawRectangle(ul[0],ul[1],dr[0]-ul[0],dr[1]-ul[1])
            dc.EndDrawing()

        wx.StaticBitmap(self, -1, self.bmp)
        
    def OnRightClick(self, e):


        wx.StaticBitmap(self, -1, self.bmp_orig)
#        reset PULLUTE VERSION to CLEAN VERSION
        self.bmp = self.bmp_orig
        self.positions[:] =[]
        

              


