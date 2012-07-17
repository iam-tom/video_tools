import os
import wx
import wdManager


import iwx



#Configure GUI - to import and convert video files
#__________________________________________________________
#Member Variables:
#	wd_settings ...........  [basepath,name]
#       vid_settings ...........  [basepath,name,author,scenes,res,fps,desc]

#
#Methods:
#	OnOpen()...........


class MainWindow(wx.Frame):
    def __init__(self, parent, title):


#----presets

       # self.wd_settings=list(2)

        #self.vid_settings=list(6)
        
        self.WD = wdManager.wd_cfg()
        self.VCFG = wdManager.vid_cfg()




        codec_preset_display=["-","mpeg2","h.264"]
        self.codec_preset_intern=[" "," -c:v mpeg2"," -c:v lib264"]

	res_preset_display=["-","hd 720p","hd 1080p"]
	self.res_preset_intern=[" "," -s 1280x720"," -s 1920x1080"]

	bv_preset_display=["-","3000kb/s","1000kb/s"]
	self.bv_preset_intern=[" " ," -b:v 3000K"," -b:v 10000K"]
#----graphical components
        wx.Frame.__init__(self, parent, title=title, size=(700,600))



#adding 2 vertical panels
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(splitter, -1)
        self.panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)

        vbox1.Add(self.panel12, 1, wx.EXPAND)
        panel1.SetSizer(vbox1)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(splitter, -1)
        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)

        vbox2.Add(panel22, 1, wx.EXPAND)
        panel2.SetSizer(vbox2)

        hbox.Add(splitter, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.SetSizer(hbox)
        self.CreateStatusBar()
        splitter.SplitVertically(panel1, panel2)
        self.Centre()

#txt controls
#console
        st2 = wx.StaticText(panel22, -1, 'Console', (7, 390))
        self.console = iwx.iConsole(panel22,style=wx.TE_MULTILINE, pos = (7, 410), size= (330,120))

	dummy1 = wx.StaticText(self.panel12,-1,"__Files to be imported___",(7,7))
        self.console.out( "No files selected")

#listctrl

        self.LC =iwx.iList(self.panel12,(200,200),(7,7),["Name"])

#status bar
        self.CreateStatusBar() # A StatusBar in the bottom of the window
#menu

        filemenu= wx.Menu()


        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        


        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Settings") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

#buttons
        b_process=wx.Button(self.panel12,wx.ID_ANY,"Import",(270,480),(70,30),wx.BU_EXACTFIT)


#checkbox
        self.chkbx = wx.CheckBox(self.panel12,wx.ID_ANY,"Convert",pos=(7,240))

#choice
	s_codec=wx.StaticText(self.panel12,wx.ID_ANY,"Codec",pos=(7,270))	
        self.choice_codec=wx.Choice(self.panel12, wx.ID_ANY, pos= (7,290), size=(70,30), choices=codec_preset_display)
	s_codec=wx.StaticText(self.panel12,wx.ID_ANY,"Resolution",pos=(7,330))
        self.choice_res=wx.Choice(self.panel12, wx.ID_ANY, pos= (7,350), size=(70,30), choices=res_preset_display)
        s_bv=wx.StaticText(self.panel12,wx.ID_ANY,"Video Quality",pos=(7,390))
        self.choice_bv=wx.Choice(self.panel12, wx.ID_ANY, pos= (7,410), size=(70,30), choices=bv_preset_display)

#WD STUFF~~~~~~~~~~~~~~
        dummy_wd=wx.StaticText(panel22,wx.ID_ANY,"Working Directory: Browse for existing WD \n  or chose path for new WD.",pos=(7,10))

        wd_b_reset=wx.Button(panel22,wx.ID_ANY,"Reset",(250,60),(70,30),wx.BU_EXACTFIT)

	wd_dummy1 = wx.StaticText(panel22,-1,"__________",(7,50))
	self.wd_s_path = iwx.iStaticText(panel22,-1,"Path:",(7,110))
	self.wd_s_name = iwx.iStaticText(panel22,-1,"Name:",(7,170))
	self.wd_s_desc = iwx.iStaticText(panel22,-1,"Description:",(7,230))

        wd_b_browse=wx.Button(panel22,wx.ID_ANY,"Browse",(150,60),(70,30),wx.BU_EXACTFIT)

        self.Show(True)

        self.Bind(wx.EVT_BUTTON, self.OnResetWD,wd_b_reset)
        self.Bind(wx.EVT_BUTTON, self.OnBrowseWD,wd_b_browse)
        self.Bind(wx.EVT_BUTTON, self.OnProcess, b_process)



# OnbBrowseWD()   
    def OnBrowseWD(self,e):

        dir_dlg = wx.DirDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
           self.WD.basepath = dir_dlg.GetPath()
           #self.WDdirname  = dir_dlg.GetPath()
          # self.WDpath = self.WDdirname
           self.console.out("Path set to: %s" % self.WD.basepath,"good")
	   self.wd_s_path.AddString("%s" % self.WD.basepath)
        dir_dlg.Destroy()
        os.chdir(self.WD.basepath)
        
        if os.path.isfile(".wd") == True:
            self.console.out("WD detected","good")
            # read in .wd file and setup wd_settings
        else:
            self.console.out("setting up new WD","good")
            self.OnEditNameWD()




# OnReset()
    def OnResetWD(self,e):
	self.wd_s_path.Clear()
	self.wd_s_name.Clear()
        self.WD.path = ""
	self.WD.name = ""
	self.console.out("Project settings cleared","bad")
	

#OnEditNameWD()
    def OnEditNameWD(self):
        dlg = wx.TextEntryDialog(self, 'Enter Project Name','Name')
        dlg.SetValue("%s" % self.WD.name)
        if dlg.ShowModal() == wx.ID_OK:
            self.WD.name = dlg.GetValue()
            self.WD.basepath = self.WD.basepath +"/" +self.WD.name
	    self.wd_s_name.AddString("%s" % self.WD.name)
            self.console.out("Name set to: %s " % self.WD.name,"good")
        dlg.Destroy()      


            
    #def wd_CreateProjectConfig(self):
        
     #   self.project_config =[self.project_path,self.project_name , "08/08/08","iam.tom","2","24","1280x720"]


#~~~~~~~~~~~~~~~~WD STUFF END

#-----callback methods
# OnAbout()
    def OnAbout(self,e):


        dlg = wx.MessageDialog( self, "Create default working directory for video editing", "About cnf_gui", wx.OK)
        dlg.ShowModal() 
        dlg.Destroy() 


# OnWDNew
    def OnWDNew(self,e):
        print "to be implemented"
# OnWDOld
    def OnWDOld(self,e):
        print "to be implemented"
        



# OnProcess()
    def OnProcess(self,e):
	self.console.out("creating new WD")
        proj = wdManager.Project_Creator(self.WD,self.VCFG)
        proj.CreateNewProject()
	self.console.out("done","good")
        do_convert = False

        list_paths=self.LC.GetPaths()
        list_names=self.LC.GetNames()
        if len(list_paths) == 0:
            self.console.out("No files chosen. Import not possible","error")

        if self.chkbx.IsChecked() == True:
            do_convert = True
            target_res_string =self.res_preset_intern[self.choice_res.GetCurrentSelection()]
            target_codec_string = self.codec_preset_intern[self.choice_codec.GetCurrentSelection()]
            target_bv_string = self.bv_preset_intern[self.choice_bv.GetCurrentSelection()]
            target_list =[target_codec_string,target_res_string,target_bv_string]
        else:

            target_list=[" "," " ," "]
        self.console.out("Importing Videos to WD...")     
        k=0   
        for i in list_paths:
            input_name= list_names[k]
            input_file = i
            cp_string=self.CpString(input_name,i,self.WD.basepath)
            os.system(cp_string)
            k=k+1
        self.console.out("Done Importing","good")
        if do_convert == True:
            k=0
            self.console.out("Converting Videos.\n This may take a while.")
            for i in list_paths:
                 input_name= list_names[k]
                 input_file = i
                 avconv_string=self.AvconvString(input_name,self.WD.basepath,target_list)
                 print avconv_string
                 os.system(avconv_string)
                 k=k+1
                 #print avconv_string
                 self.console.out("Converting %s" % input_name)


            self.console.out("Done Converting.","good")
        #avconv_string = AvconvString(target_list)
            

#AvconvString()
    def AvconvString(self,input_name,WD,target_list):
        acs="avconv -i "+WD+"/files/video/raw/"+input_name+ target_list[0]+target_list[1]+target_list[2]+" -strict experimental "+WD+"/files/video/conv/"+input_name
        return acs       	    
#CpString()
    def CpString(self,input_name,input_path,WD):
        cps="cp "+input_path+" "+WD+"/files/video/raw/"+input_name
        return cps


        


app = wx.App(False)
frame = MainWindow(None, "Configuration GUI")
app.MainLoop()
