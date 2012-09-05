import os
import wx
import wd
import avtools
import GUIelements

import iwx

import utils


#Configure GUI - to import and convert video files
#__________________________________________________________
#Member Variables:
#	wd_settings ......  [basepath,name]
#       vid_settings ......  [basepath,name,author,scenes,res,fps,desc]

#
#Methods:
#	OnOpen()......


class wdGUI(wx.Panel):
    def __init__(self, parent, config):
#presets

        self.WD = wd.wd_cfg()
        
        self.list_paths = list()
        self.list_names = list()

        codec_preset_display=["-","mpeg2","h.264"]
        self.codec_preset_intern=[" ",".mpeg",".mov"]

        res_preset_display=["-","hd 720p","hd 1080p"]
        self.res_preset_intern=[" ","1280x720","1920x1080"]

    	bv_preset_display=["-","3000kb/s","1000kb/s"]
        self.bv_preset_intern=[" " ,"3000K","10000K"]
	    
	    
#----graphical components

        wx.Panel.__init__(self, parent, size=config["size"])


#//////////////// PUBSUB /////////
 

        
#buttons
        b_process=wx.Button(self,wx.ID_ANY,"Import",(270,480),(70,30),wx.BU_EXACTFIT)


#checkbox
        self.chkbx = wx.CheckBox(self,wx.ID_ANY,"Convert",pos=(7,310))

#choice
	s_codec=wx.StaticText(self,wx.ID_ANY,"Codec",pos=(7,330))	
        self.choice_codec=wx.Choice(self, wx.ID_ANY, pos= (7,350), size=(70,30), choices=codec_preset_display)
#	s_codec=wx.StaticText(self,wx.ID_ANY,"Resolution",pos=(7,390))
#        self.choice_res=wx.Choice(self, wx.ID_ANY, pos= (7,410), size=(70,30), choices=res_preset_display)
        self.choice_res=GUIelements.iChoice(self,(7,390),"res")
        s_bv=wx.StaticText(self,wx.ID_ANY,"Video Quality",pos=(7,450))
        self.choice_bv=wx.Choice(self, wx.ID_ANY, pos= (7,470), size=(70,30), choices=bv_preset_display)

#WD STUFF~~~~~~~~~~~~~~
        dummy_wd=wx.StaticText(self,wx.ID_ANY,"Working Directory: Browse for existing WD \n  or chose path for new WD.",pos=(7,10))

        wd_b_reset=wx.Button(self,wx.ID_ANY,"Reset",(7,60),(70,30),wx.BU_EXACTFIT)
        wd_b_browse=wx.Button(self,wx.ID_ANY,"Browse",(150,60),(70,30),wx.BU_EXACTFIT)

	wd_dummy1 = wx.StaticText(self,-1,"_________________________",(7,80))
	self.wd_s_path = iwx.iStaticText(self,-1,"Path:",(7,110))
	self.wd_s_name = iwx.iStaticText(self,-1,"Name:",(7,170))
	self.wd_s_desc = iwx.iStaticText(self,-1,"Details:",(7,230))
	wd_dummy1 = wx.StaticText(self,-1,"_________________________",(7,290))       


        wd_b_desc=wx.Button(self,wx.ID_ANY,"View / Edit",(7,270),(100,30),wx.BU_EXACTFIT)

        self.Show(True)

        self.Bind(wx.EVT_BUTTON, self.OnResetWD,wd_b_reset)
        self.Bind(wx.EVT_BUTTON, self.OnBrowseWD,wd_b_browse)
        self.Bind(wx.EVT_BUTTON, self.OnProcess, b_process)
        self.Bind(wx.EVT_BUTTON, self.OnEditDesc, wd_b_desc)
        



# OnbBrowseWD()   
    def OnBrowseWD(self,e):

        dir_dlg = wx.DirDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
           self.WD.basepath = dir_dlg.GetPath()
           #self.WDdirname  = dir_dlg.GetPath()
          # self.WDpath = self.WDdirname

	   self.wd_s_path.AddString("%s" % self.WD.basepath)
        dir_dlg.Destroy()
        os.chdir(self.WD.basepath)
        self.project = wd.Project_Creator()
        if os.path.isfile(".wd") == True:
            
            self.project.ReadWDFile(self.WD)

            self.WD.old_wd = True
            
        else:

            dlg = wx.TextEntryDialog(self, 'Enter Project Name','Name')
            dlg.SetValue("%s" % self.WD.name)
            if dlg.ShowModal() == wx.ID_OK:
                self.WD.name = dlg.GetValue()
                self.WD.basepath = self.WD.basepath +"/" +self.WD.name

                dlg.Destroy()
        self.setGUItoWD(self.WD)
        

    def setGUItoWD(self,WD):
        self.wd_s_path.Clear()
        self.wd_s_name.Clear()
        self.wd_s_desc.Clear()
        self.wd_s_path.AddString(WD.basepath)
        self.wd_s_name.AddString(WD.name)  


# OnReset()
    def OnResetWD(self,e):
	self.wd_s_path.Clear()
	self.wd_s_name.Clear()
        self.WD.path = ""
	self.WD.name = ""



            
    #def wd_CreateProjectConfig(self):
        
     #   selfroject_config =[selfroject_path,selfroject_name , "08/08/08","iam.tom","2","24","1280x720"]


#~~~~~~~~~~~~~~~~WD STUFF END

#-----callback methods


    def SetInPath(self,msg):
        self.list_paths = msg[0]
        self.list_names = msg[1]
        print self.list_paths 

# OnEditDesc()
    def OnEditDesc(self,e):

        vdesc = descGUI(self,self.WD)
        if vdesc.ShowModal() == 5:            
           dumbass=0
        self.setGUItoWD(self.WD)
        
        

# OnProcess()
    def OnProcess(self,e):        
        do_convert = False
        if self.WD.done == False:

            self.project.CreateNewProject(self.WD)

            self.WD.done = True




        if len(self.list_paths) == 0:
            print "Choose input files first"

        if self.chkbx.IsChecked() == True:
            Converter = avtools.converter()
            do_convert = True
            av_config={"format":".mov","zeros":3,"i_path":"","o_path":"","frame_size":"vga","fps":50,"bv":"10000K"}
            av_config["frame_size"]=self.choice_res.GetChoice()
            av_config["frame_size"]=""# OVERRIDE TO BE FIXED
            
            av_config["format"]= self.codec_preset_intern[self.choice_codec.GetCurrentSelection()]
            av_config["format"]= ".MOV"
            av_config["bv"] = self.bv_preset_intern[self.choice_bv.GetCurrentSelection()]

      

            


        for i in range(len(self.list_paths)):
            input_name= self.list_names[i]
            input_file = self.list_paths[i]
            cp_string=self.CpString(input_name,input_file,self.WD.basepath)
            utils.assert_dir(self.WD.basepath)
            os.system(cp_string)


        if do_convert == True:


            for i in range(len(self.list_paths)):
                input_name= self.list_names[i]
                input_file = self.list_paths[i]
                self.AvconvString(input_name,self.WD.basepath,av_config)                
                print "config"
                print av_config
                
                Converter.UpdateConfig(av_config)  
                print "converting file %i of %i"%(i,len(self.list_paths))
                Converter.Run()








            

#AvconvString()
    def AvconvString(self,input_name,WD,config):
        config["o_path"] = WD+"/files/video/conv/"
        config["i_path"] = list()
        config["i_path"].append(WD+"/files/video/raw/"+input_name) 
        

       	    
#CpString()
    def CpString(self,input_name,input_path,WD):
        cps="cp "+input_path+" "+WD+"/files/video/raw/"
        #cps="cp "+input_path+" "+WD+"/files/video/raw/"+input_name
        return cps


        


class descGUI(wx.Dialog):
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



