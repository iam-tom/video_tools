import sys
import wx
import iwx
import cStringIO
from PIL import Image
from wx.lib.pubsub import Publisher
from TimeLapseTools import tlm
from av_tools import thumbnailer


class GUI(wx.Panel):
    def __init__(self, parent,config):
    
#//////////////// allocations /////////////////

        self.positions = list()
    
        self.in_path = config["i_file"]
        self.size = config["size"]
        
        self.init_img = ".data/tlm_init.png"
        
#//////////////// graphical elements /////////        
        p_size=(self.size[0],self.size[1])

        wx.Panel.__init__(self, parent,size=p_size)
#        button panel
        b_accept=wx.Button(self,wx.ID_OK,"OK",(0,(self.size[1]*4)/5),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,lambda  evt , config = config: self.OnAccept(evt,config))
        
       

        
        self.setInitState()
        
#//////////////// TLM ///////////

        
        
#//////////////// PUBSUB /////////
 
        Publisher().subscribe(self.OnFilesMsg,"master.filesmsg") 
 
 
 
 
 
#///////////CALLBACKS /////////////

    def OnFilesMsg(self,msg):
        self.setNewState(msg.data[0][0]) 
                        

    def setNewState(self,in_path):
        
#     wipe canvas   
            
            

    #        CLEAN VERISION
            imageFile = in_path
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
        print image.GetWidth()
        print image.GetHeight()
        

        bmp = wx.BitmapFromImage(image)

        self.canvas =wx.StaticBitmap(self, -1, bmp, (0, 0))
    
    def scale_image(self,image):
        o_width = image.GetWidth()
        o_height = image.GetHeight()
        print o_width
        print self.size[0]
        q = float(self.size[0]) /float( o_width)
        new_width = self.size[0]
        new_height = o_height*q
        
        if new_height*5 > self.size[1]*4:
            print "rescaling"
            new_height = (self.size[1]*4)/5
            print new_height
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
   
        Publisher().sendMessage(("imgGUI.positions"), self.positions)    


    def OnLeftClick(self, e):


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
        elif len(self.positions) == 3:
            dim_box1=(self.positions[1][0]- self.positions[0][0],self.positions[1][1]- self.positions[0][1])
            ul = self.positions[2]
            dr = (self.positions[2][0]+dim_box1[0],self.positions[2][1]+dim_box1[1])
            dc.BeginDrawing()
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
    def __init__(self,parent,i_size,i_pos,i_col_list):
        self.L =iwx.iList(parent,i_size,i_pos,i_col_list)
        b_prev=wx.Button(parent,wx.ID_ANY,"Preview",(i_size[0]+20,160),(70,30),wx.BU_EXACTFIT)
        b_prev.Bind(wx.EVT_BUTTON, self.OnPrev,b_prev)
        self.T = thumbnailer()
        self.prev_init_state(parent,(i_size[0]+140, 60))
        wx.StaticText(parent,wx.ID_ANY,"Preview",pos=(i_size[0]+140,40))	

        

        
    def prev_init_state(self,parent,pos):
        self.config = {"format":".png","frame_size":"qvga", "i_path":"", "o_path":"/tmp/" }

        bmp  = self.get_bmp(".data/prev_init.png")
        self.canvas =wx.StaticBitmap(parent, -1, bmp,pos )    

    def get_bmp(self,path):
        data = open(path, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        image = wx.ImageFromStream( stream )  

        bmp = wx.BitmapFromImage(image)
        return bmp
                
    def OnPrev(self,e):
        
        index = self.L.get_selected()
        self.config["i_path"] = self.L.path_list[index[0]]
        
        self.T.UpdateConfig(self.config)
        self.T.CreateThumbnail()
        
        bmp = self.get_bmp("/tmp/thb"+self.config["format"])
       
        self.canvas.SetBitmap( bmp)
              


