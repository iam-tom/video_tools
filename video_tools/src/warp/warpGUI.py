
import wx




class warpGUI(wx.Panel):

    def __init__(self,parent):
    
    
    
    #default vaules-----------------------------------------------------
    
    
#WARP TEST        #self.init_img=wx.Image("../../src/.data/tlm_init.bmp",wx.BITMAP_TYPE_ANY,-1)
        self.init_img=wx.Image(".data/warp_init.png",wx.BITMAP_TYPE_PNG,-1)
        self.init_zoom_img=wx.Image(".data/warp_zoom.png",wx.BITMAP_TYPE_PNG,-1)
        size_over=wx.Size(600,400)
        size_zoom=wx.Size(200,200)
    
    # layout ---------------------------------------
    #####PANELS
       #parent panel p1  
        wx.Panel.__init__(self,parent)
    ######BOX SIZERS

        #bs1=wx.BoxSizer(wx.VERTICAL)
        bs1=wx.FlexGridSizer(rows=3,cols=1)
        #bs1.SetFlexibleDirection(wx.VERTICAL)
        bs11=wx.BoxSizer(wx.HORIZONTAL)
        bs12=wx.BoxSizer(wx.HORIZONTAL)
        bs13=wx.BoxSizer(wx.HORIZONTAL)
         
        
    ###### LAYOUT PANEL 11
        self.button_up11=wx.Button(self,-1,"U\nP",size=(30,200))


        img=self.init_img.Scale(size_over[0],size_over[1],wx.IMAGE_QUALITY_HIGH)
        self.over11=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))
        
        bs111=wx.FlexGridSizer(rows=3,cols=1)
        img=self.init_zoom_img.Scale(size_zoom[0],size_zoom[1],wx.IMAGE_QUALITY_HIGH)
        self.zoom11=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))        
        
        bs1111=wx.BoxSizer(wx.HORIZONTAL)
        
        bs1111.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)
        bs1111.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)

        self.list11=wx.ListBox(self,-1,size=(200,170))        

        bs111.Add(self.zoom11,wx.EXPAND,1)
        bs111.Add(bs1111,wx.EXPAND,1)
        bs111.Add(self.list11,wx.EXPAND,1)
        bs111.AddGrowableRow(0,0)
        bs111.AddGrowableRow(2,0)

        bs11.Add(self.over11     , wx.ALIGN_TOP ,0)
        bs11.Add(bs111           , wx.ALIGN_TOP ,0)
        bs11.Add(self.button_up11, wx.ALIGN_TOP ,0)
    ###### LAYOUT PANEL 11

        self.button_down12=wx.Button(self,-1,"D\nO\nW\nN",size=(30,200))

        img=self.init_img.Scale(size_over[0],size_over[1],wx.IMAGE_QUALITY_HIGH)
        self.over12=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))
        
        #bs121=wx.BoxSizer(wx.VERTICAL)
        bs121=wx.FlexGridSizer(rows=3,cols=1)

        img=self.init_zoom_img.Scale(size_zoom[0],size_zoom[1],wx.IMAGE_QUALITY_HIGH)
        self.zoom12=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))        
        
        bs1211=wx.BoxSizer(wx.HORIZONTAL)
        
        bs1211.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)
        bs1211.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)

        self.list12=wx.ListBox(self,-1,size=(200,170))        

        bs121.Add(self.zoom12,wx.EXPAND,1)
        bs121.Add(bs1211,wx.CENTER,1)
        bs121.Add(self.list12,wx.EXPAND,1)
        bs121.AddGrowableRow(0,0)
        bs121.AddGrowableRow(2,0)


        bs12.Add(self.over12     , wx.ALIGN_TOP ,0)
        bs12.Add(bs121           , wx.ALIGN_TOP ,0)
        bs12.Add(self.button_down12, wx.ALIGN_LEFT ,0)

    ###### LAYOUT PANEL 12
        

    ###### LAYOUT PANEL 13
        self.button_up13    =wx.Button(self)
        self.button_down13   =wx.Button(self)
        
        bs13.Add(self.button_up13  ,wx.EXPAND)
        bs13.Add(self.button_down13,wx.EXPAND)

    ###### MAKE LAYOUT

        bs1.Add(bs11,1,wx.ALIGN_LEFT) 
        bs1.Add(bs12,1,wx.ALIGN_TOP) 
        bs1.Add(bs13,1,wx.ALIGN_BOTTOM) 
        bs1.AddGrowableRow(0,0)
        bs1.AddGrowableRow(1,0)
        #bs1.AddGrowableRow(2,0)
        #self.SetAutoLayout(True)
        self.SetSizer(bs1)
        self.Layout()
        self.Fit()
