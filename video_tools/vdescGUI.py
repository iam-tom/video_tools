import os
import wx
import wdManager

import iwx



#Configure GUI - to set up working directory (wd) creation
#__________________________________________________________
#Member Variables:
#	name............... project name

#
#Methods:
#	OnOpen()...........


class GUI(wx.Dialog):
    def __init__(self, parent, WD):
        self.WD = WD
        self.cont = False
       # wx.Frame.__init__(self, parent, title="Project Details", size=(300,500))
        wx.Dialog.__init__(self, parent, title="Project Details", size=(300,500))

# default settings


#status bar
        #self.CreateStatusBar() # A StatusBar in the bottom of the window
#menu

        filemenu= wx.Menu()


        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")



        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
       # self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

#buttons
        b_name=wx.Button(self,wx.ID_ANY,"Edit",(7,70),(50,25),wx.BU_EXACTFIT)
        b_date=wx.Button(self,wx.ID_ANY,"Edit",(7,130),(50,25),wx.BU_EXACTFIT)
        b_author=wx.Button(self,wx.ID_ANY,"Edit",(7,190),(50,25),wx.BU_EXACTFIT)
	b_scenes=wx.Button(self,wx.ID_ANY,"Edit",(7,250),(50,25),wx.BU_EXACTFIT)
	b_fps=wx.Button(self,wx.ID_ANY,"Edit",(7,310),(50,25),wx.BU_EXACTFIT)
	b_res=wx.Button(self,wx.ID_ANY,"Edit",(7,370),(50,25),wx.BU_EXACTFIT)

        b_name_c=wx.Button(self,wx.ID_ANY,"Clear",(67,70),(50,25),wx.BU_EXACTFIT)
        b_date_c=wx.Button(self,wx.ID_ANY,"Clear",(67,130),(50,25),wx.BU_EXACTFIT)
        b_author_c=wx.Button(self,wx.ID_ANY,"Clear",(67,190),(50,25),wx.BU_EXACTFIT)
	b_scenes_c=wx.Button(self,wx.ID_ANY,"Clear",(67,250),(50,25),wx.BU_EXACTFIT)
	b_fps_c=wx.Button(self,wx.ID_ANY,"Clear",(67,310),(50,25),wx.BU_EXACTFIT)
	b_res_c=wx.Button(self,wx.ID_ANY,"Clear",(67,370),(50,25),wx.BU_EXACTFIT)

	b_reset=wx.Button(self,wx.ID_ANY,"Reset",(7,410),(50,25),wx.BU_EXACTFIT)

	b_accept=wx.Button(self,5,"Accept",(67,410),(50,25),wx.BU_EXACTFIT)

#static text
        s_dummy1 = wx.StaticText(self,-1,"Video Configuration:",(7,20))

	self.s_name = iwx.iStaticText(self,-1,"Name:",(7,50))
	self.s_date = iwx.iStaticText(self,-1,"Creation Date:",(7,110))
	self.s_author = iwx.iStaticText(self,-1,"Author:",(7,170))
	self.s_scenes = iwx.iStaticText(self,-1,"# of scenes:",(7,230))
	self.s_fps = iwx.iStaticText(self,-1,"fps:",(7,290))
	self.s_res = iwx.iStaticText(self,-1,"Resolution:",(7,350))
#events
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        b_name.Bind(wx.EVT_BUTTON, lambda evt,string=self.s_name,att="name": self.OnEdit(evt, string,att) )
        b_author.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_author,att="author": self.OnEdit(evt, string,att) )
	b_date.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_date,att="date": self.OnEdit(evt, string,att) )
	b_scenes.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_scenes,att="scenes": self.OnEdit(evt, string,att) )
	b_fps.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_fps,att="fps": self.OnEdit(evt, string,att) )
	b_res.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_res,att="res": self.OnEdit(evt, string,att) )

	b_name_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_name: self.OnClear(evt, string) )
	b_author_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_author: self.OnClear(evt, string) )
	b_date_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_date: self.OnClear(evt, string) )
	b_scenes_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_scenes: self.OnClear(evt, string) )
	b_scenes_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_scenes: self.OnClear(evt, string) )
	b_fps_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_fps: self.OnClear(evt, string) )
	b_res_c.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_res: self.OnClear(evt, string) )


	b_reset.Bind(wx.EVT_BUTTON,  self.OnReset )
	b_accept.Bind(wx.EVT_BUTTON,  self.OnAccept )


	#self.Bind(wx.EVT_BUTTON, self.OnProcess,b_process)
	self.s_name.AddString(self.WD.name)
	self.s_date.AddString(self.WD.date)
	self.s_author.AddString(self.WD.author)
	self.s_scenes.AddString(self.WD.scenes)
	self.s_fps.AddString(self.WD.fps)
	self.s_res.AddString(self.WD.res)




        self.Show(True)


# OnAbout()
    def OnAbout(self,e):
        names= ("a","b")
        size=(100,100)
        num_cats=2
        setup_list=[size,num_cats,names]
        a=iwx.iForm(setup_list)





# OnExit()
    def OnExit(self,e):

        self.Close(True)  # Close the frame.
        

#OnEdit()
    def OnEdit(self,e,string,att):
        dlg = wx.TextEntryDialog(self, 'Enter Project Name','Name')
        #dlg.SetValue("%s" % self.name)
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()
            string.Clear()
	    string.AddString("%s" % value )        
        dlg.Destroy()
        self.WD.set_attribute(att,value)
        

#OnClear()
    def OnClear(self,e,string):
            string.Clear()

#OnReset()
    def OnReset(self,e):
        self.s_name.Clear()
        self.s_author.Clear()
        self.s_date.Clear()
        self.s_fps.Clear()
        self.s_scenes.Clear()
        self.s_res.Clear()

    def OnAccept(self,e):
        
        self.MakeModal(False)
        self.cont = True
   
        self.Close()



