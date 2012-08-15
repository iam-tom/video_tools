import os
import wx
import wdManager
import av_tools


import iwx



#Configure GUI - to import and convert video files
#__________________________________________________________
#Member Variables:
#	wd_settings ......  [basepath,name]
#       vid_settings ......  [basepath,name,author,scenes,res,fps,desc]

#
#Methods:
#	OnOpen()......


class GUI(wx.Panel):
    def __init__(self, parent, config):
#presets

        self.WD = wdManager.wd_cfg()
        
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
	s_codec=wx.StaticText(self,wx.ID_ANY,"Resolution",pos=(7,390))
        self.choice_res=wx.Choice(self, wx.ID_ANY, pos= (7,410), size=(70,30), choices=res_preset_display)
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
        self.project = wdManager.Project_Creator()
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
        import vdescGUI

        vdesc = vdescGUI.GUI(self,self.WD)
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
            Converter = av_tools.converter()
            do_convert = True
            av_config={"format":".mov","zeros":3,"i_path":"","o_path":"","frame_size":"vga","fps":50,"bv":"10000K"}
            av_config["frame_size"]=self.res_preset_intern[self.choice_res.GetCurrentSelection()]
            av_config["format"]= self.codec_preset_intern[self.choice_codec.GetCurrentSelection()]
            av_config["bv"] = self.bv_preset_intern[self.choice_bv.GetCurrentSelection()]

      

            


        for i in range(len(self.list_paths)):
            input_name= self.list_names[i]
            input_file = self.list_paths[i]
            cp_string=self.CpString(input_name,input_file,self.WD.basepath)
            print "copying"
            os.system(cp_string)


        if do_convert == True:


            for i in range(len(self.list_paths)):
                input_name= self.list_names[i]
                input_file = self.list_paths[i]
                self.AvconvString(input_name,self.WD.basepath,av_config)
                raw_input("1")
                Converter.UpdateConfig(av_config)
                print av_config
                raw_input("2")
                Converter.Convert()
                raw_input("3")







            

#AvconvString()
    def AvconvString(self,input_name,WD,config):
        config["o_path"] = WD+"/files/video/conv/"
        config["i_path"] = list()
        config["i_path"].append(WD+"/files/video/raw/"+input_name) 
        

       	    
#CpString()
    def CpString(self,input_name,input_path,WD):
        cps="cp "+input_path+" "+WD+"/files/video/raw/"+input_name
        return cps


        


