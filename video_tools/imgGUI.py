import sys
import wx
import cStringIO
from PIL import Image



class GUI(wx.Panel):
    def __init__(self, parent,size,in_path):    
        self.positions = list()
        wx.Panel.__init__(self, parent,size=size)

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
        self.bmp = wx.BitmapFromImage( wx.ImageFromStream( stream ))
        # show the bitmap, (5, 5) are upper left corner coordinates
        self.img =wx.StaticBitmap(self, -1, self.bmp, (0, 0))
        self.img.Bind(wx.EVT_LEFT_DOWN,self.OnLeftClick)
        self.img.Bind(wx.EVT_RIGHT_DOWN,self.OnRightClick)


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
        
    def GetBoxes(self):
        return self.positions      


