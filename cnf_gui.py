import os
import wx
import wdm_module

import iwx



#Configure GUI - to set up working directory (wd) creation
#__________________________________________________________
#Member Variables:
#	name............... project name
#	desc............... project description
#	path............... folder wd is created in
#	config_list........ list, describing the project settings
#	
#	s_name............. iStaticText to display name
#	s_path............. iStaticText to display path
#	s_desc............. iStaticText to display desc
#
#	b_name............. Button to browse for folder
#	b_name............. Button to edit name
#	b_desc............. Button to edit description
#
#	b_reset............ Button to reset project settings
#	b_process.......... Button to start processing
#
#	console............ iConsole to display system messages
#
#	panel12............ left panel, structuring elements
#	panel22............ right panel, structuring elements
#
#Methods:
#	OnOpen()...........
#	OnReset()..........
#	OnEditName().......
#	OnEditDesc().......
#	OnExit()...........
#	OnAbout()..........
#	OnProcess()........ Interface to wdm_module
#	CreateConfigList... Create list, containing project configuration

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(700,400))

#default value for name
	self.name="project"
        self.desc=""
# ONLY DEBUG
#	self.path = "/home/goa-tz/python_workspace"

#adding 2 vertical panels
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(splitter, -1)
        self.panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
        st1 = wx.StaticText(self.panel12, -1, 'File', (5, 5))
        vbox1.Add(self.panel12, 1, wx.EXPAND)
        panel1.SetSizer(vbox1)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(splitter, -1)
        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)
        st2 = wx.StaticText(panel22, -1, 'Console', (7, 185))
        vbox2.Add(panel22, 1, wx.EXPAND)
        panel2.SetSizer(vbox2)

        hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.SetSizer(hbox)
        self.CreateStatusBar()
        splitter.SplitVertically(panel1, panel2)
        self.Centre()

#txt controls
#creating console
        self.console = iwx.iConsole(panel22,style=wx.TE_MULTILINE, pos = (7, 210), size= (330,120))

	dummy1 = wx.StaticText(self.panel12,-1,"__________",(7,7))
	self.s_path = iwx.iStaticText(self.panel12,-1,"Path:",(7,50))
	self.s_name = iwx.iStaticText(self.panel12,-1,"Name:",(7,110))
	self.s_desc = iwx.iStaticText(self.panel12,-1,"Description:",(7,170))


        self.console.out( "Path is not defined. Use the path menu entry")

#status bar
        self.CreateStatusBar() # A StatusBar in the bottom of the window
#menu

        filemenu= wx.Menu()


        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        menuPath = filemenu.Append(wx.ID_OPEN,"&Path","Set basepath")
        menuProcess = filemenu.Append(wx.ID_DEFAULT,"&Process","Create")


        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Settings") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

#buttons
        b_process=wx.Button(self.panel12,wx.ID_ANY,"Process",(270,300),(70,30),wx.BU_EXACTFIT)
        b_reset=wx.Button(self.panel12,wx.ID_ANY,"Reset",(190,300),(70,30),wx.BU_EXACTFIT)
        b_browse=wx.Button(self.panel12,wx.ID_ANY,"Browse",(7,70),(70,30),wx.BU_EXACTFIT)
        b_name=wx.Button(self.panel12,wx.ID_ANY,"Edit",(7,130),(70,30),wx.BU_EXACTFIT)
        b_desc=wx.Button(self.panel12,wx.ID_ANY,"Edit",(7,190),(70,30),wx.BU_EXACTFIT)

#events
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuPath)

	self.Bind(wx.EVT_BUTTON, self.OnProcess,b_process)
        self.Bind(wx.EVT_BUTTON, self.OnReset,b_reset)
        self.Bind(wx.EVT_BUTTON, self.OnOpen,b_browse)
        self.Bind(wx.EVT_BUTTON, self.OnEditName,b_name)
        self.Bind(wx.EVT_BUTTON, self.OnEditDesc,b_desc)

        self.Show(True)


# OnAbout()
    def OnAbout(self,e):


        dlg = wx.MessageDialog( self, "Create default working directory for video editing", "About cnf_gui", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.



# OnExit()
    def OnExit(self,e):
        self.Close(True)  # Close the frame.

# OnOpen()   
    def OnOpen(self,e):

        dir_dlg = wx.DirDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        if dir_dlg.ShowModal() == wx.ID_OK:

           self.dirname  = dir_dlg.GetPath()
           self.path = self.dirname
           self.console.out("Path set to: %s" % self.path,"good")
	   self.s_path.AddString("%s" % self.path)

        dir_dlg.Destroy()


# OnProcess()
    def OnProcess(self,e):
        try:
	    self.path
        except AttributeError:
            self.path="EMPTY"
        
        if self.path == "EMPTY":
         
           self.console.out( "Path still needs to be set!" ,"error")

        else:
            tempname=self.path+"/"+self.name

            self.console.out( "Processing..." )
            self.CreateConfigList()           
            manager= wdm_module.wdm(tempname,self.config_list)
            manager.CreateWD()
            self.console.out( "...done" )

# OnReset()
    def OnReset(self,e):
	self.s_path.Clear()
	self.s_name.Clear()
        self.path = "EMPTY"
	self.name = "project"
	self.console.out("Project settings cleared","bad")
	

#OnEditName()
    def OnEditName(self,e):
        dlg = wx.TextEntryDialog(self, 'Enter Project Name','Name')
        dlg.SetValue("%s" % self.name)
        if dlg.ShowModal() == wx.ID_OK:
            self.name = dlg.GetValue()
	    self.s_name.AddString("%s" % self.name)
            self.console.out("Name set to: %s " % self.name,"good")
        dlg.Destroy()
        

#OnEditDesc()
    def OnEditDesc(self,e):
        dlg = wx.TextEntryDialog(self,"Project Description","Project Description")
        dlg.SetValue("%s" % self.desc )
        if dlg.ShowModal() == wx.ID_OK:
            self.desc = dlg.GetValue()
	    self.s_desc.AddString("set")
            self.console.out("Descrition added","good")
        dlg.Destroy()

            
    def CreateConfigList(self):
        
        self.config_list =[self.name , "08/08/08","iam.tom","2","24","1280x720"]

        


app = wx.App(False)
frame = MainWindow(None, "Configuration GUI")
app.MainLoop()
