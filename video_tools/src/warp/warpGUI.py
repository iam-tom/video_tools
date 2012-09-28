
import wx

import iwx
import GUIelements


class frame(wx.StaticBitmap):
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
        print "[frame]tbi check_log"
        
          
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
        print "[frame]tbi save_log"
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
            ## image coordinates of middle of canvas.
            self.offset = wx.Point(0,0)
    # Bind position callback to canvas
            self.Bind(wx.EVT_LEFT_DOWN,self.PosCallback)
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
    ##
    # Set offset to middle of current image.
    # Can be used to ensure valid image coordinates, when
    # only crop of original image is displayed.
    # @param self object pointer
    # @param offset image coordinates of middle of canvas.
    def set_offset(self,offset):
        self.offset=offset

    def scale(self):
        return self.scale_

    def pos(self):
        return self.pos_
# Callback stuff ----------------------------------
    def PosCallback(self,e):
        pos=wx.Point(e.GetPosition().x*self.scale()+self.offset.x,e.GetPosition().y*self.scale()+self.offset.y)
        evt =iwx.iEvent(iwx.EVT_POS_pub,1,pos)
        self.GetEventHandler().ProcessEvent(evt)
class warpGUI(wx.Panel):


    def __init__(self,parent):
    #default vaules-----------------------------------------------------
        self.in_path=list()
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/01_2000.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/02_2000.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9942.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9943.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9944.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9954.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9955.JPG")

    #make layout and activate bidnings
        self.make_layout(parent)
        self.set_init_state()
        self.set_test_state(0,1)
        self.make_bindings()


    def make_layout(self,parent):
    # layout ---------------------------------------
        size_over=wx.Size(600,400)
        size_zoom=wx.Size(200,200)

    #parent panel p1  
        wx.Panel.__init__(self,parent)
    #BOX SIZERS

        bs1=wx.FlexGridSizer(rows=4,cols=1)
        bs11=wx.BoxSizer(wx.HORIZONTAL)
        bs12=wx.BoxSizer(wx.HORIZONTAL)
        bs13=wx.BoxSizer(wx.HORIZONTAL)
         
        
    ###### LAYOUT PANEL 0--------------------------------------
        self.button_up11=wx.Button(self,-1,"U\nP",size=(30,200))


        self.over0=canvas(self,size_over)

        bs111=wx.FlexGridSizer(rows=3,cols=1)

        self.zoom0=canvas(self,size_zoom)        
        
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
    ###### LAYOUT PANEL 1------------------------------------
 
        self.button_down12=wx.Button(self,-1,"D\nO\nW\nN",size=(30,200))

        self.over1=canvas(self,size_over)
        
        bs121=wx.FlexGridSizer(rows=3,cols=1)

        self.zoom1=canvas(self,size_zoom)
        
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

    ###### LAYOUT Bottom PANEL 
        self.button_up13    =wx.Button(self,-1,"BUT!")
        self.button_down13   =wx.Button(self,-1,"BUT!")
        
        bs13.Add(self.button_up13  ,wx.EXPAND)
        bs13.Add(self.button_down13,wx.EXPAND)

    ##### LAYOUT NAVPANEL
        self.nav = GUIelements.iNavpanel(self,3)
    ###### MAKE LAYOUT

        bs1.Add(bs11,1,wx.ALIGN_LEFT) 
        bs1.Add(self.nav,1,wx.EXPAND)
        bs1.Add(bs12,1,wx.ALIGN_TOP) 
        bs1.Add(bs13,1,wx.ALIGN_BOTTOM) 
        bs1.AddGrowableRow(0,0)
        bs1.AddGrowableRow(1,0)

        self.SetSizer(bs1)
        self.Layout()
        self.Fit()


    def make_bindings(self):
    #BINDINGS-------------------------------------------------------------------
        # bindings to move focus of zoom
        self.over0.Bind(iwx.EVT_POS_sub,lambda evt, frame = self.f0 ,canvas=self.zoom0: self.ZoomCallback(evt,frame,canvas))
        self.over1.Bind(iwx.EVT_POS_sub,lambda evt, frame = self.f1 ,canvas=self.zoom1: self.ZoomCallback(evt,frame,canvas))
        #bindings for pixel picking
        self.zoom0.Bind(iwx.EVT_POS_sub,lambda evt, frame = self.f0 , canvas = self.over0 : self.PointCallback(evt,frame,canvas))
        self.zoom1.Bind(iwx.EVT_POS_sub,lambda evt, frame = self.f1 , canvas = self.over1 : self.PointCallback(evt,frame,canvas))

        # bindings for frame up<-->down
        self.button_up11.Bind(wx.EVT_BUTTON, self.OnFrameUp)
        self.button_down12.Bind(wx.EVT_BUTTON, self.OnFrameDown)
        self.nav.forward.Bind(iwx.EVT_INC_sub,self.OnFrameSwitch)
        self.nav.back.Bind(iwx.EVT_INC_sub,self.OnFrameSwitch)

    #~~~~~~~Functionality~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        


    def ZoomCallback(self,e,frame,canvas):
        pos=e.GetVal()
        pos = wx.Point(pos.x-canvas.size().x/2,pos.y-canvas.size().y/2)
        self.set_zoom(frame,canvas,pos)
    def PointCallback(self, e,frame,canvas):

        pos = e.GetVal()
        dc = wx.MemoryDC() 
        bitmap=wx.BitmapFromImage(frame.img())
        a= dc.SelectObject(bitmap)
        dc.BeginDrawing()
        dc.SetPen(wx.Pen("red",style=wx.SOLID,width=5))
        dc.SetBrush(wx.Brush("red", wx.TRANSPARENT))
        #dc.DrawRectangle(pos[0],pos[1],30,30)
        dc.DrawCircle(pos[0],pos[1],25)
        dc.EndDrawing()
        img=wx.ImageFromBitmap(bitmap)
        canvas.draw(img)
        print pos 

    def OnFrameUp(self,e):
        new_id0=self.f0.id()+1
        new_id1=self.f1.id()+1    
        if new_id1>=len(self.in_path):
            print "last frame..."
            return
        self.set_state(new_id0,new_id1)

        self.over0.draw(self.f0.img())
        self.nav.modifyCtr(self.nav.GetCtr()+1)

    def OnFrameDown(self,e):
        new_id0=self.f0.id()-1
        new_id1=self.f1.id()-1    
        if new_id0<0:
            print "first frame..."
            return
        self.set_state(new_id0,new_id1)
        self.nav.modifyCtr(self.nav.GetCtr()-1)

    def OnFrameSwitch(self,e):
        val=int(e.GetVal())
        new_id0=self.f0.id()+val
        new_id1=self.f1.id()+val    
        if new_id0<0:
            print "first frame..."
            return
        if new_id1>=len(self.in_path):
            print "last frame..."
            return
        else:    
            self.set_state(new_id0,new_id1)

    def set_state(self,id0,id1):

        if id0 ==self.f1.id() and id1<>self.f0.id() and id1<>self.f1.id():
             self.f0=self.f1
             self.f1=frame(self.in_path[id1],id1)
        
        elif id0 ==self.f0.id()  and id1<>self.f0.id() and id1<>self.f1.id():
             self.f1=frame(self.in_path[id1],id1)

        elif id1 ==self.f0.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f1=self.f0
             self.f0=frame(self.in_path[id0],id0)

        elif id1 ==self.f1.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f0=frame(self.in_path[id0],id0)

        elif id0 ==self.f0.id()  and id1==self.f1.id() :
             self.f0=self.f0
             self.f1=self.f1

        else:
                if id0 <0 or id1 < 0:
                    return
                self.f0=frame(self.in_path[id0],id0)
                self.f1=frame(self.in_path[id1],id1)
        self.over0.draw(self.f0.img())
        self.over1.draw(self.f1.img())
        #TODO: hard coded initial point of zoom --make middle of frame
        self.set_zoom(self.f0,self.zoom0,wx.Point(1000,1000))
        self.set_zoom(self.f1,self.zoom1,wx.Point(1000,1000))

        # update bindings!
        self.make_bindings()
    
    def set_test_state(self,id0,id1):

        self.f0=frame(self.in_path[id0],id0)
        self.f1=frame(self.in_path[id1],id1)

        self.over0.draw(self.f0.img())
        self.set_zoom(self.f0,self.zoom0,wx.Point(1000,1000))

        self.over1.draw(self.f1.img())
        self.set_zoom(self.f1,self.zoom1,wx.Point(1000,1000))
        
        #update navbar
        self.nav.SetSteps(len(self.in_path)-1)
    def set_init_state(self):

        init_img="../../src/.data/tlm_init.bmp"
        init_img_zoom="../../src/.data/warp_zoom.png"
        self.f0=frame(init_img,-1)
        self.f1=frame(init_img,-1)


        zoom_init_frame=frame(init_img_zoom,-1)

        self.over0.draw(self.f0.img())
        self.zoom0.draw(zoom_init_frame.img())

        self.over1.draw(self.f1.img())
        self.zoom1.draw(zoom_init_frame.img())


    def set_zoom(self,frame,canvas,pos):
        rec = list()
        dr = pos+(int(canvas.size().x/2),int(canvas.size().y/2))
        ul = pos+(-int(canvas.size().x/2),-int(canvas.size().y/2)) 
        
        ## Make sure crop is n bounds
        #if ul.x <0:
        #    ul.x=0
        #    dr.x=canvas.size().x
        #if ul.y < 0:
        #    ul.y = 0
        #    dr.y=canvas.size().y
        #if dr.x > frame.size().x:
        #    ul.x = frame.size().x - canvas.size().x
        #    dr.x = frame.size().x
        #if dr.y > frame.size().y:
        #    dr.y = frame.size().y        
        #    ul.y = frame.size().y -canvas.size().y       

        rec.append(ul)    
        rec.append(dr)    
        crop = frame.img().GetSubImage(wx.Rect(pos.x,pos.y,canvas.size().x,canvas.size().y))

        canvas.draw(crop)
        canvas.set_offset(pos)
        sel_pts=list()
        pts=frame.pts() 
        for i in range(len(pts)):
            if (pts[i].x > ul.x and pts[i].x < dr.x) and (pts[i].y > ul.y and pts[i].y < dr.y):
                sel_pts.append(pts[i]-pos)
                

    def draw_pts(self,pts,canvas):
        print"tbi drav_pts"                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
