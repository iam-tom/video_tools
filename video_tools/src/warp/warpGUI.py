
import wx
import utils
import imgutils
import iwx
import GUIelements
import os
import warp

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
        self.morphed_path=list()
        self.out_path = "/home/tom/warptest/"
        self.tmp_path= "/tmp/warpGUI/"
        utils.assert_dir(self.tmp_path)
        self.transformations=list()

    #make layout and activate bidnings
        self.make_layout(parent)
        self.set_init_state()
        self.set_test_state(0,1)
        self.make_bindings()

    def SetInPath(self,msg):
        self.in_path = msg[0]
        self.set_state(0,1)
        self.nav.SetSteps(len(self.in_path))
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
        self.button_exe    =wx.Button(self,-1,"PROCESS")
        self.button_down13   =wx.Button(self,-1,"--")
        

    ##### LAYOUT NAVPANEL
        bs_nav=wx.BoxSizer(wx.HORIZONTAL)
        self.nav = GUIelements.iNavpanel(self,3)
        bs_nav.Add(self.nav  ,wx.EXPAND)
        bs_nav.Add(self.button_exe  ,wx.EXPAND)
        bs_nav.Add(self.button_down13,wx.EXPAND)
        
    ###### MAKE LAYOUT

        bs1.Add(bs11,1,wx.ALIGN_LEFT) 
        bs1.Add(bs_nav,1,wx.EXPAND)
        bs1.Add(bs12,1,wx.ALIGN_TOP) 
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
        
        # bindings for processing
        self.button_exe.Bind(wx.EVT_BUTTON, self.OnExe)
        self.button_down13.Bind(wx.EVT_BUTTON,self.OnAccept)

    #~~~~~~~Functionality~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        


    def ZoomCallback(self,e,frame,canvas):
        pos=e.GetVal()
        pos = wx.Point(pos.x-canvas.size().x/2,pos.y-canvas.size().y/2)
        self.set_zoom(frame,canvas,pos)

    ##
    # @brief Callback for point on canvas
    # 
    # Gets click position and ads it to frame
    # @param self Object pointer
    # @param e Event
    # @param frame Frame, point is in
    def PointCallback(self, e,frame,canvas):
        pos = e.GetVal()
        frame.add_pts(pos)
        self.draw_pts(frame,canvas)

    ##
    # @brief draw points of frame
    def draw_pts(self,frame,canvas):
        dc = wx.MemoryDC() 
        bitmap=wx.BitmapFromImage(frame.img())
        a= dc.SelectObject(bitmap)
        dc.BeginDrawing()
        radius=5*canvas.scale()
        penwidth=5*canvas.scale()
        dc.SetPen(wx.Pen("red",style=wx.SOLID,width=penwidth))
        dc.SetBrush(wx.Brush("red", wx.TRANSPARENT))
        dc.SetTextForeground("red")
        dc.SetFont(wx.Font(int(10*canvas.scale()), wx.SWISS, wx.NORMAL, wx.BOLD))
        pt_ctr=0
        for pt in frame.pts():
            dc.DrawCircle(pt.x,pt.y,radius)
            ctr_pos=wx.Point(pt.x+(10*canvas.scale()),pt.y+(10*canvas.scale()))
            dc.DrawTextPoint(str(pt_ctr),ctr_pos)
            pt_ctr+=1
        dc.EndDrawing()
        img=wx.ImageFromBitmap(bitmap)
        canvas.draw(img)
            
        
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
        # set frames f0 and f1 
        if id0 ==self.f1.id() and id1<>self.f0.id() and id1<>self.f1.id():
             self.f0=self.f1
             self.f1=iwx.iFrame(self.in_path[id1],id1)
        
        elif id0 ==self.f0.id()  and id1<>self.f0.id() and id1<>self.f1.id():
             self.f1=iwx.iFrame(self.in_path[id1],id1)

        elif id1 ==self.f0.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f1=self.f0
             self.f0=iwx.iFrame(self.in_path[id0],id0)

        elif id1 ==self.f1.id()  and id0<>self.f0.id() and id0<>self.f1.id():
             self.f0=iwx.iFrame(self.in_path[id0],id0)

        elif id0 ==self.f0.id()  and id1==self.f1.id() :
             self.f0=self.f0
             self.f1=self.f1

        else:
                if id0 <0 or id1 < 0:
                    return
                self.f0=iwx.iFrame(self.in_path[id0],id0)
                self.f1=iwx.iFrame(self.in_path[id1],id1)
        #update GUI
        self.over0.draw(self.f0.img())
        self.over1.draw(self.f1.img())
        #TODO: hard coded initial point of zoom --make middle of frame
        self.set_zoom(self.f0,self.zoom0,wx.Point(1000,1000))
        self.set_zoom(self.f1,self.zoom1,wx.Point(1000,1000))
        # draw points 
        self.draw_pts(self.f0,self.over0)
        self.draw_pts(self.f1,self.over1)

        # update bindings!
        self.make_bindings()
    
    def set_test_state(self,id0,id1):
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9942.JPG")
        self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9943.JPG")
        #self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9944.JPG")
        #self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9954.JPG")
        #self.in_path.append("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/IMG_9955.JPG")

        self.f0=iwx.iFrame(self.in_path[id0],id0)
        self.f1=iwx.iFrame(self.in_path[id1],id1)

        self.over0.draw(self.f0.img())
        self.set_zoom(self.f0,self.zoom0,wx.Point(1000,1000))

        self.over1.draw(self.f1.img())
        self.set_zoom(self.f1,self.zoom1,wx.Point(1000,1000))
        
        #update navbar
        self.nav.SetSteps(len(self.in_path)-1)
    def set_init_state(self):

        init_img=".data/warp_init.png"
        init_img_zoom=".data/warp_zoom.png"
        self.f0=iwx.iFrame(init_img,-1)
        self.f1=iwx.iFrame(init_img,-1)


        zoom_init_frame=iwx.iFrame(init_img_zoom,-1)

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


    def OnExe(self,e):
        m=warp.morpher()
        m.SetInputFrames(self.f0,self.f1)
        m.Run(trafo_only=True)
        self.transformations.append(m.GetTrafo())
    # save init_frame
        if self.f0.id()==0:
            m.Run()
            o_file=self.tmp_path+"imgm"+str(self.f0.id())+".jpg"
            self.f0.SaveImg(o_file)
            self.morphed_path.append(o_file)
        else:
            for i in range(self.f1.id()):
                if i ==0:
                   T=self.transformations[0] 
                else:
                    T=imgutils.trafo_combine(T,self.transformations[i])
                    m.Run(T)
        o_file=self.tmp_path+"imgm"+str(self.f1.id())+".jpg"
        m.SaveImgM(o_file)
        self.morphed_path.append(o_file)

    def OnAccept(self,e):
        w=warp.warper()
        config={"i_path":self.morphed_path,"o_path":"/home/tom/TEST/","warp_frames":70,"o_type":".jpg"}
        w.UpdateConfig(config)
        pairs=len(self.morphed_path)-1
        if pairs<=3 and pairs > 1:
            w.Run_parallel(num_proc=pairs)
        elif pairs>3:
            w.Run_parallel(num_proc=3)
        else:
            w.Run()
    
    def CleanTmp(self,e):
        os.system("rm -rf /tmp/warpGUI/*")
        os.system("rm -rf /tmp/frames/*")


