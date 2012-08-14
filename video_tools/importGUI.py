import os
import wx
import wdManager



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
        self.codec_preset_intern=[" "," -c:v mpeg2"," -c:v lib264"]

        res_preset_display=["-","hd 720p","hd 1080p"]
        self.res_preset_intern=[" "," -s 1280x720"," -s 1920x1080"]

    	bv_preset_display=["-","3000kb/s","1000kb/s"]
        self.bv_preset_intern=[" " ," -b:v 3000K"," -b:v 10000K"]
	    
	    
#----graphical components

        wx.Panel.__init__(self, parent, size=config["size"])


#//////////////// PUBSUB /////////
 

        
#buttons
        b_process=wx.Button(self,wx.ID_ANY,"Import",(270,480),(70,30),wx.BU_EXACTFIT)


#checkbox
        self.chkbx = wx.CheckBox(self,wx.ID_ANY,"Convert",pos=(7,240))

#choice
	s_codec=wx.StaticText(self,wx.ID_ANY,"Codec",pos=(7,270))	
        self.choice_codec=wx.Choice(self, wx.ID_ANY, pos= (7,290), size=(70,30), choices=codec_preset_display)
	s_codec=wx.StaticText(self,wx.ID_ANY,"Resolution",pos=(7,330))
        self.choice_res=wx.Choice(self, wx.ID_ANY, pos= (7,350), size=(70,30), choices=res_preset_display)
        s_bv=wx.StaticText(self,wx.ID_ANY,"Video Quality",pos=(7,390))
        self.choice_bv=wx.Choice(self, wx.ID_ANY, pos= (7,410), size=(70,30), choices=bv_preset_display)

#WD STUFF~~~~~~~~~~~~~~
        dummy_wd=wx.StaticText(self,wx.ID_ANY,"Working Directory: Browse for existing WD \n  or chose path for new WD.",pos=(7,10))

        wd_b_reset=wx.Button(self,wx.ID_ANY,"Reset",(250,60),(70,30),wx.BU_EXACTFIT)

	wd_dummy1 = wx.StaticText(self,-1,"__________",(7,50))
	self.wd_s_path = iwx.iStaticText(self,-1,"Path:",(7,110))
	self.wd_s_name = iwx.iStaticText(self,-1,"Name:",(7,170))
	self.wd_s_desc = iwx.iStaticText(self,-1,"Details:",(7,230))
	wd_dummy1 = wx.StaticText(self,-1,"__________",(7,245))       

        wd_b_browse=wx.Button(self,wx.ID_ANY,"Browse",(150,60),(70,30),wx.BU_EXACTFIT)
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
        selfroject = wdManager.Project_Creator()
        if os.path.isfile(".wd") == True:
            
            selfroject.ReadWDFile(self.WD)

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

            selfroject.CreateNewProject(self.WD)

            self.WD.done = True




        if len(list_paths) == 0:
            print "Choose input files first"

        if self.chkbx.IsChecked() == True:
            do_convert = True
            target_res_string =self.res_preset_intern[self.choice_res.GetCurrentSelection()]
            target_codec_string = self.codec_preset_intern[self.choice_codec.GetCurrentSelection()]
            target_bv_string = self.bv_preset_intern[self.choice_bv.GetCurrentSelection()]
            target_list =[target_codec_string,target_res_string,target_bv_string]
        else:

            target_list=[" "," " ," "]

        k=0   
        for i in list_paths:
            input_name= list_names[k]
            input_file = i
            cp_string=self.CpString(input_name,i,self.WD.basepath)
            os.system(cp_string)
            k=k+1

        if do_convert == True:
            k=0

            for i in list_paths:
                 input_name= list_names[k]
                 input_file = i
                 avconv_string=self.AvconvString(input_name,self.WD.basepath,target_list)
                 print avconv_string
                 os.system(avconv_string)
                 k=k+1
                 #print avconv_string




        #avconv_string = AvconvString(target_list)
            

#AvconvString()
    def AvconvString(self,input_name,WD,target_list):
        acs="avconv -i "+WD+"/files/video/raw/"+input_name+ target_list[0]+target_list[1]+target_list[2]+" -strict experimental "+WD+"/files/video/conv/"+input_name
        return acs       	    
#CpString()
    def CpString(self,input_name,input_path,WD):
        cps="cp "+input_path+" "+WD+"/files/video/raw/"+input_name
        return cps


        


