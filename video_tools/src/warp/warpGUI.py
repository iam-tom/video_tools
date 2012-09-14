
import wx


class frame():
#//////////////////////<<<INIT////////////////////////////////////////////
    def __init__(self,path,id):
        self.img_orig_=wx.Image(path,wx.BITMAP_TYPE_ANY)
        self.img_work_=self.img_orig_.Copy()
        self.pts_=list()
        self.check_log()
        self.id_=id
        self.size_=self.img_orig_.GetSize()
#//////////////////////<<<METHODS///////////////////////////////////////
    def check_log(self):
        print "tbi check_log"
        
          
    #    pts_log=list()
    #TODO: if id exists
    #        open logifile and read pts
    #        self.add_pts(pts_log)
    #    else:
    #        self.save_log()

    def add_pts(self,pts):
        self.pts.append(pts)
        self.save_log()

    def save_log(self):
        #TODO: save log with sel.id
        print "tbi save_log"
    def reset_hard(self):
    #Warning use with caution - log is being deleted - otherwise use reset
        self.img_work_=img.orig_.Copy()
        self.pts=list()
        self.save_log()

    def reset(self):
        self.img_work_=img.orig_.Copy()
        self.pts=list()

#//////////////////////<<<GETTERS///////////////////////////////////////
    def img(self):
        return self.img_work_
    
    def pts(self):
        return self.pts_  
   
    def id(self):
        return self.id_     

    def size(self):
        return self.size_

class canvas(wx.StaticBitmap):
    def __init__(self,parent,size):
            wx.StaticBitmap.__init__(self,parent,size=size)
            self.scale_=float()            
            self.size_=size
    def size(self):
        return self.size_
    
    def set_scale(self,img):
        so=self.size()
        si=img.GetSize()
       #TODO min of si/so is scale.... 
        scale = float(si.x)/float(so.x)
        self.scale_= scale 
    
    def draw(self,img):
        img_scaled=img.Scale(self.size_.x,self.size_.y,wx.IMAGE_QUALITY_HIGH)
        self.set_scale(img)
        self.SetBitmap(wx.BitmapFromImage(img_scaled))

    def scale(self):
        return self.scale_
class warpGUI(wx.Panel):

    def __init__(self,parent):
    
    
    
    #default vaules-----------------------------------------------------
    
    
        self.init_img=wx.Image("../../src/.data/tlm_init.bmp",wx.BITMAP_TYPE_ANY,-1)
       # self.init_img=wx.Image(".data/warp_init.png",wx.BITMAP_TYPE_PNG,-1)
        self.init_zoom_img=wx.Image("../../src/.data/warp_zoom.png",wx.BITMAP_TYPE_PNG,-1)
        self.in_path=list()
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/01_2000.JPG")

        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/02_2000.JPG")
        self.make_layout(parent)
        self.set_first_state(0,1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~11111111111111111~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~11111111111111111~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # layout ---------------------------------------
    def make_layout(self,parent):
        size_over=wx.Size(600,400)
        size_zoom=wx.Size(200,200)
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


        self.over0=canvas(self,size_over)
        self.over0.draw(self.init_img) 

        bs111=wx.FlexGridSizer(rows=3,cols=1)
        img=self.init_zoom_img.Scale(size_zoom[0],size_zoom[1],wx.IMAGE_QUALITY_HIGH)
        #self.zoom0=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))        
        self.zoom0=canvas(self,size_zoom)        
        self.zoom0.draw(self.init_zoom_img) 
        
        bs1111=wx.BoxSizer(wx.HORIZONTAL)
        
        bs1111.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)
        bs1111.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)

        self.list11=wx.ListBox(self,-1,size=(200,170))        

        bs111.Add(self.zoom0,wx.EXPAND,1)
        bs111.Add(bs1111,wx.EXPAND,1)
        bs111.Add(self.list11,wx.EXPAND,1)
        bs111.AddGrowableRow(0,0)
        bs111.AddGrowableRow(2,0)

        bs11.Add(self.over0     , wx.ALIGN_TOP ,0)
        bs11.Add(bs111           , wx.ALIGN_TOP ,0)
        bs11.Add(self.button_up11, wx.ALIGN_TOP ,0)
    ###### LAYOUT PANEL 11

        self.button_down12=wx.Button(self,-1,"D\nO\nW\nN",size=(30,200))

        img=self.init_img.Scale(size_over[0],size_over[1],wx.IMAGE_QUALITY_HIGH)
        self.over1=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))
        
        #bs121=wx.BoxSizer(wx.VERTICAL)
        bs121=wx.FlexGridSizer(rows=3,cols=1)

        img=self.init_zoom_img.Scale(size_zoom[0],size_zoom[1],wx.IMAGE_QUALITY_HIGH)
        self.zoom1=wx.StaticBitmap(self,-1,wx.BitmapFromImage(img))        
        
        bs1211=wx.BoxSizer(wx.HORIZONTAL)
        
        bs1211.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)
        bs1211.Add(wx.Button(self,-1,"BUT!"),wx.EXPAND)

        self.list12=wx.ListBox(self,-1,size=(200,170))        

        bs121.Add(self.zoom1,wx.EXPAND,1)
        bs121.Add(bs1211,wx.CENTER,1)
        bs121.Add(self.list12,wx.EXPAND,1)
        bs121.AddGrowableRow(0,0)
        bs121.AddGrowableRow(2,0)


        bs12.Add(self.over1     , wx.ALIGN_TOP ,0)
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

#BINDINGS/////////////////////////////////////////////////////////////////
        self.over0.Bind(wx.EVT_LEFT_DOWN,self.OnLClick)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~22222222222222222~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~22222222222222222~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def OnLClick(self,e):
    # TEST BINDING TO SET ZOOM
        pos_scaled=e.GetPosition()
        print pos_scaled
        print self.over0.scale()
        pos=wx.Point((pos_scaled.x*self.over0.scale())-self.zoom0.size().x/2,(pos_scaled.y*self.over0.scale()-self.zoom0.size().y/2))
        print pos
        self.set_zoom(self.f0,self.zoom0,pos)
    def OnFrameUp(self):
        new_id0=self.f0.id()+1
        new_id1=self.f1.id()+1    
        if id1>=len(self.in_paths):
            print "last frame..."
            return
        set_state(new_id0,new_id1)

        self.over0.draw(self.f0.img())
    def OnFrameDown(self):
        new_id0=self.f0.id()-1
        new_id1=self.f1.id()-1    
        if id0<0:
            print "first frame..."
            return
        set_state(new_id0,new_id1)

    def set_state(self,id0,id1):

        if id0 ==self.f1.id() and id1<>self.f0.id() and id1<>self.f1.id():
             self.f0=self.f1
             self.f1=frame(self.in_path[id1],id1)
        
        elif id0 ==self.f0.id()  and id1<>self.f0.id() and id1<>self.f1.id():
             self.f1=frame(self.in_path[id1],id1)

        elif id1 ==self.f0.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f1=self.f0
             self.f0=frame(self.in_path[id0],i0)

        elif id1 ==self.f1.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f0=frame(self.in_path[id0],i0)

        elif id0 ==self.f0.id()  and id1==self.f1.id() :
             self.f0=self.f0
             self.f1=self.f1

        else:
                if id0 <0 or id1 < 0:
                    return
                self.f0=frame(self.in_path[id0],id0)
                self.f1=frame(self.in_path[id1],id1)

        self.draw_canvas(self.f0.img(),self.over0)
        self.draw_canvas(self.f1.img(),self.over1)
        self.draw_pts(self.f0.pts(),self.over0)
        self.draw_pts(self.f1.pts(),self.over1)
    
    def set_first_state(self,id0,id1):

        self.f0=frame(self.in_path[id0],id0)
        self.f1=frame(self.in_path[id1],id1)

        self.draw_canvas(self.f0.img(),self.over0)
        self.over0.draw(self.f0.img())
        
        self.set_zoom(self.f0,self.zoom0,wx.Point(1000,1000))

        self.draw_canvas(self.f1.img(),self.over1)
        self.draw_pts(self.f0.pts(),self.over0)
        self.draw_pts(self.f1.pts(),self.over1)
        
        #self.set_zoom(self.f0,self.zoom0,wx.Point(100,100))


    def set_zoom(self,frame,canvas,pos):
        rec = list()
        dr = pos+(int(canvas.size().x/2),int(canvas.size().y/2))
        ul = pos+(-int(canvas.size().x/2),-int(canvas.size().y/2)) 
        # Make sure crop is n bounds
        if ul.x <0:
            ul.x=0
            dr.x=canvas.size().x
        if ul.y < 0:
            ul.y = 0
            dr.y=canvas.size().y
        if dr.x > frame.size().x:
            ul.x = frame.size().x - canvas.size().x
            dr.x = frame.size().x
        if dr.y > frame.size().y:
            dr.y = frame.size().y        
            ul.y = frame.size().y -canvas.size().y       

        rec.append(ul)    
        rec.append(dr)    
        #crop = frame.img().crop(rec)
        crop = frame.img().GetSubImage(wx.Rect(pos.x,pos.y,canvas.size().x,canvas.size().y))

        self.draw_canvas(crop,canvas)
        canvas.draw(crop)
        sel_pts=list()
        pts=frame.pts() 
        for i in range(len(pts)):
            if (pts[i].x > ul.x and pts[i].x < dr.x) and (pts[i].y > ul.y and pts[i].y < dr.y):
                sel_pts.append(pts[i]-pos)
                

    def draw_canvas(self,img,canvas):
        print "tbi draw_canvas"
    def draw_pts(self,pts,canvas):
        print"tbi drav_pts"                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
