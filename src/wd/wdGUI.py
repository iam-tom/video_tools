import os
import wx
import wd
import avtools
import GUIelements

import iwx

import utils

from threading import Thread


#Configure GUI - to import and convert video files
#__________________________________________________________
#Member Variables:
#	wd_settings ......  [basepath,name]
#       vid_settings ......  [basepath,name,author,scenes,res,fps,desc]

#
#Methods:
#	OnOpen()......


class wdGUI(wx.Panel):
    def __init__(self, parent):
#presets

        self.WD = wd.wd_cfg()
        
        self.list_paths = list()
        self.list_names = list()
        self.choices={"codec":["mpeg2","h.264"],"codec_lookup":[".mpeg",".mov"],
                      "bitrate":["3000kb/s","10.000kb/s"],"bitrate_lookup":["3000K","10000K"],
                      "scale":["hd720p","hd 1080p"],"scale_lookup":["1280x720","1920x1080"],
                      "fps":  ["24 fps","25 fps" , "50 fps"],"fps_lookup":["24","25","50"]  }
    

        self.make_layout(parent)
        self.make_bindings()

    def make_layout(self,parent):
        wx.Panel.__init__(self, parent)
        fgs0 =wx.FlexGridSizer(rows=2,cols=2)
        bs0  =wx.BoxSizer(wx.VERTICAL)
        bs1  =wx.BoxSizer(wx.VERTICAL)
        bs2  =wx.BoxSizer(wx.VERTICAL)



        self.b_reset=wx.Button(  self,-1,"Reset",(70,30))
        self.b_browse=wx.Button( self,-1,"Browse",(70,30))
        self.b_desc=wx.Button(   self,-1,"View / Edit",(100,30))


        space=wx.Size(100,100)
        self.chkbx = wx.CheckBox(self,wx.ID_ANY,"Convert video files")
        self.choice_codec=wx.Choice(self,    wx.ID_ANY, size=(100,30), choices=self.choices["codec"])
        self.choice_bitrate=wx.Choice(self,  wx.ID_ANY, size=(100,30), choices=self.choices["bitrate"])
        self.choice_scale=wx.Choice(self,    wx.ID_ANY, size=(100,30), choices=self.choices["scale"])
        self.choice_fps=wx.Choice(self,      wx.ID_ANY, size=(100,30), choices=self.choices["fps"])

        
        self.wd_s_path = iwx.iStaticText(self,-1,"Path:")
        self.wd_s_name = iwx.iStaticText(self,-1,"Name:")
        self.wd_s_desc = iwx.iStaticText(self,-1,"Details:")
        wd_dummy1 = wx.StaticText(self,-1,"_________________________")       
        self.b_process=wx.Button(self,-1,"Import",(70,30))




        bs0.Add(self.b_browse)
        bs0.Add(self.b_desc)
        bs0.Add(self.b_reset)

        bs1.Add(space)
        bs1.Add(self.chkbx)
        bs1.Add(self.choice_codec)        
        bs1.Add(self.choice_bitrate)        
        bs1.Add(self.choice_scale)        
        bs1.Add(self.choice_fps)        
        bs1.Add(self.b_process)
    
        bs2.Add(wd_dummy1)
        bs2.Add(self.wd_s_path)
        bs2.Add(self.wd_s_name)
        bs2.Add(self.wd_s_desc)


        fgs0.Add(bs0)
        fgs0.Add(bs2)
        fgs0.Add(bs1) 

        self.SetSizer(fgs0)
        self.Layout()
        self.Fit()








        self.Show(True)

    def make_bindings(self):
        self.Bind(wx.EVT_BUTTON, self.OnResetWD,self.b_reset)
        self.Bind(wx.EVT_BUTTON, self.OnBrowseWD,self.b_browse)
        self.Bind(wx.EVT_BUTTON, self.OnProcess, self.b_process)
        self.Bind(wx.EVT_BUTTON, self.OnEditDesc, self.b_desc)
        



# OnbBrowseWD()   
    def OnBrowseWD(self,e):

        dir_dlg = wx.DirDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
           self.WD.basepath = dir_dlg.GetPath()

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
                self.WD.basepath = self.WD.basepath +utils.delimiter +self.WD.name+utils.delimiter

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
            av_config={"format":".mov","zeros":3,"i_path":"","o_path":"","frame_size":"vga","fps":24,"bv":"10000K"}

            av_config["format"]=self.choices["codec_lookup"][self.choice_codec.GetCurrentSelection()]
            av_config["bv"]=self.choices["bitrate_lookup"][self.choice_codec.GetCurrentSelection()]
            av_config["frame_size"]=self.choices["scale_lookup"][self.choice_codec.GetCurrentSelection()]
            av_config["fps"]=self.choices["fps_lookup"][self.choice_codec.GetCurrentSelection()]

            


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
                Thread(target=Converter.Run()).start()








            

#AvconvString()
    def AvconvString(self,input_name,WD,config):
        config["o_path"] = WD+utils.delimiter+"files"+utils.delimiter+"video"+utils.delimiter+"conv"
        config["i_path"] = list()
        config["i_path"].append(WD+utils.delimiter+"files"+utils.delimiter+"video"+ utils.delimiter+"raw"+utils.delimiter+input_name) 
        

       	    
#CpString()
    def CpString(self,input_name,input_path,WD):
        cps="cp "+input_path+" "+WD+"files"+utils.delimiter+"video"+utils.delimiter+"raw"+utils.delimiter
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



