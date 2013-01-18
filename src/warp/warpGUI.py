
import wx
import utils
import imgutils
import iwx
import GUIelements
import os
import warp

class warpGUI(wx.Panel):
    def __init__(self,parent,size):
    #default vaules-----------------------------------------------------

    #TODO: This layout is specifically for images with 3/2 image ratio:w
        self.input_image_ratio = 1.5 # = 3/2

        self.in_path=list()
        self.morphed_path=list()
        #self.out_path = "/home/tom/warptest/"
        tmp=utils.temp_dir_handler()
        self.tmp_path=utils.folder_back+utils.folder_back+ "tmp"+utils.delimiter+"warpGUI"
        tmp.add_dir(self.tmp_path,"pre-clean")
        self.transformations=list()
        # flag for trafo of current state
        self.trafo_valid=False

    #make layout and activate bidnings
        self.make_layout(parent,size)
        self.set_init_state()
        #self.set_test_state(0,1)
        self.make_bindings()

    def SetInPath(self,msg):
        self.in_path = msg[0]
        self.set_state(0,1)
        self.nav.SetSteps(len(self.in_path)-2)
        self.make_bindings()
    def make_layout(self,parent,fsize):
    # layout ---------------------------------------
        
        over_height=fsize.height*0.4
        over_width=over_height*self.input_image_ratio

        zoom_width=over_width*0.25
        zoom_height=zoom_width


        size_over=wx.Size(over_width,over_height)
        size_zoom=wx.Size(zoom_width,zoom_height)

    #parent panel p1  
        wx.Panel.__init__(self,parent)
    #BOX SIZERS

        bs1=wx.FlexGridSizer(rows=4,cols=1)
        bs11=wx.BoxSizer(wx.HORIZONTAL)
        bs12=wx.BoxSizer(wx.HORIZONTAL)
        bs13=wx.BoxSizer(wx.HORIZONTAL)
         
        
    ###### LAYOUT PANEL 0--------------------------------------
        self.button_up11=wx.Button(self,-1,"U\nP",size=(30,200))


        self.over0=iwx.iCanvas(self,size_over)

        bs111=wx.FlexGridSizer(rows=3,cols=1)

        self.zoom0=iwx.iCanvas(self,size_zoom)        
        
        bs1111=wx.BoxSizer(wx.HORIZONTAL)
        
        self.ResetF0= wx.Button(self,-1,"Reset Frame")
        bs1111.Add(self.ResetF0,wx.EXPAND)
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

        self.over1=iwx.iCanvas(self,size_over)
        
        bs121=wx.FlexGridSizer(rows=3,cols=1)

        self.zoom1=iwx.iCanvas(self,size_zoom)
        
        bs1211=wx.BoxSizer(wx.HORIZONTAL)
        
        bs1211.Add(wx.Button(self,-1,"Reset Frame"),wx.EXPAND)
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
        self.button_exe    =wx.Button(self,-1,"recalculate Trafo")
        self.button_down13   =wx.Button(self,-1,"Process")


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

        # 
        self.ResetF0.Bind(wx.EVT_BUTTON,lambda e, frame =self.f0:self.OnResetFrame(e, self.f0))

    #~~~~~~~Functionality~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def OnResetFrame(self,e,frame):
        frame.reset_hard()
        self.trafo_valid_check()

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
        self.trafo_valid_check()
        #self.draw_pts(frame,canvas)



    ##
    # @brief draw points of frame
    def draw_pts(self,frame,canvas):
 
        if self.trafo_valid == True:
            color="green"
        else:
            color="red"

        dc = wx.MemoryDC() 
        bitmap=wx.BitmapFromImage(frame.img())
        a= dc.SelectObject(bitmap)
        dc.BeginDrawing()
        radius=5*canvas.scale()
        penwidth=5*canvas.scale()
        dc.SetPen(wx.Pen(color,style=wx.SOLID,width=penwidth))
        dc.SetBrush(wx.Brush(color, wx.TRANSPARENT))
        dc.SetTextForeground(color)
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
        # check validity of state and draw points 
        self.trafo_valid_check()
        self.draw_pts(self.f0,self.over0)
        self.draw_pts(self.f1,self.over1)


        # update bindings!
        self.make_bindings()
    
    def set_init_state(self):

        init_img="data"+utils.delimiter+"warp_init.png"
        init_img_zoom="data"+utils.delimiter+"warp_zoom.png"
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
        self.MorphCurrentFrames()

    def MorphCurrentFrames(self):
        print "-->morphing pair"
        m=warp.morpher()
        m.SetInputFrames(self.f0,self.f1)
        m.Run(trafo_only=True)
        if self.f0.id()>(len(self.transformations)-1):
          print "appending trafo"
          self.transformations.append(m.GetTrafo())
          append= True
        else:
          print "updating trafo"
          self.transformations[self.f0.id()]=m.GetTrafo()
          append= False
    # save init_frame
        if self.f0.id()==0:
            m.Run()
            o_file=self.tmp_path+"imgm"+str(self.f0.id())+".jpg"
            self.f0.SaveImg(o_file)
            if append == True:
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
        if append == True:
            self.morphed_path.append(o_file)

    def OnAccept(self,e):
        w=warp.warper()
        config={"i_path":self.morphed_path,"o_path":"/home/tom/TEST/","warp_frames":50,"o_type":".jpg"}
        w.UpdateConfig(config)
        pairs=len(self.morphed_path)-1
        if pairs > 5 :
            w.Run_parallel(num_proc=3)
        elif pairs >3:
            w.Run_parallel(num_proc=2)
        else:
            w.Run()
    def CleanTmp(self,e):
        os.system("rm -rf "+self.tmp_path+utils.delimiter+"*" )
        os.system("rm -rf "+utils.folder_back+utils.folder_back+"tmp"+utils.delimiter+"frames"+utils.delimiter+"*")


    def trafo_valid_check(self):
        self.trafo_valid = False
        l1=len(self.f0.pts())
        l2=len(self.f1.pts())

        if l1==l2 and l1>=3 and l2>=3:
            self.trafo_valid = True
        self.draw_pts(self.f0,self.over0)
        self.draw_pts(self.f1,self.over1)
        if self.trafo_valid == True:
          self.MorphCurrentFrames()

