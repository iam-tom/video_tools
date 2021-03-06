import os
import wx


import iwx



#GUI TITLE
#__________________________________________________________
#Member Variables:
#	name............... function

#
#Methods:
#	OnOpen()...........


class GUI(wx.Panel):
# init method _______________________________________________
    def __init__(self, parent,size,):

        wx.Panel.__init__(self, parent,size=size)

# default settings___________________________________________
	
# layout_____________________________________________________

# callbacks__________________________________________________

# internal methods___________________________________________

# interface methods__________________________________________


#buttons
#---input
        b_i_file=wx.Button(self,wx.ID_ANY,"Browse",(7,70),(70,25),wx.BU_EXACTFIT)
	self.b_i_format=wx.Choice(self,wx.ID_ANY,(7,130),(70,30),self.format_preset)
	self.b_zeros=wx.Choice(self,wx.ID_ANY,(7,190),(50,30),self.zeros_preset)

#--output
        b_o_dir=wx.Button(self,wx.ID_ANY,"Browse",(7,250),(70,25),wx.BU_EXACTFIT)
        b_o_file=wx.Button(self,wx.ID_ANY,"Edit",(7,310),(50,25),wx.BU_EXACTFIT)
	self.b_fps=wx.Choice(self,wx.ID_ANY,(7,370),(50,30),self.fps_preset)

	b_accept=wx.Button(self,wx.ID_ANY,"Accept",(67,410),(70,25),wx.BU_EXACTFIT)

#static text
        s_dummy1 = wx.StaticText(self,-1,"Video Configuration:",(7,20))

	self.s_i_file = iwx.iStaticText(self,-1,"Input Files:",(7,50))
	self.s_o_dir = iwx.iStaticText(self,-1,"Output Directory:",(7,230))
	self.s_o_file = iwx.iStaticText(self,-1,"Output Filename:",(7,290))
	self.s_zeros = iwx.iStaticText(self,-1,"Leading Zeros:",(7,170))
	self.s_format = iwx.iStaticText(self,-1,"Input File Format:",(7,110))	
	self.s_fps = iwx.iStaticText(self,-1,"Frame Rate [fps]:",(7,350))
	
#events


	b_o_dir.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_o_dir: self.OnBrowseDir(evt, string) )
	b_o_file.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_o_file: self.OnEdit(evt, string) )
	b_i_file.Bind(wx.EVT_BUTTON, lambda evt, string=self.s_i_file: self.OnBrowseFile(evt, string) )


	




	b_accept.Bind(wx.EVT_BUTTON,  self.OnAccept )


	#self.Bind(wx.EVT_BUTTON, self.OnProcess,b_process)


        self.Show(True)

#OnBrowseDir()
    def OnBrowseDir(self,e,string):
        dir_dlg = wx.DirDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        if dir_dlg.ShowModal() == wx.ID_OK:
           self.o_dir  = dir_dlg.GetPath()           
	   string.AddString("%s" % self.o_dir)
        dir_dlg.Destroy()
#OnBrowseDir()
    def OnBrowseFile(self,e,string):
        dir_dlg = wx.FileDialog(self, "\Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)

        if dir_dlg.ShowModal() == wx.ID_OK:
           self.o_dir  = dir_dlg.GetPath()           
	   string.AddString("%s" % self.o_dir)
        dir_dlg.Destroy()




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
    def OnEdit(self,e,string):
        dlg = wx.TextEntryDialog(self, 'Edit Value','Name')
        dlg.SetValue("%s" % string.GetValue())
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()
            string.Clear()
	    string.AddString("%s" % value )

        dlg.Destroy()

#OnClear()
    def OnClear(self,e,string):

        string.Clear()

#OnReset()
    def OnReset(self,e):
        self.s_i_file.Clear()
	self.s_o_dir.Clear() 
	self.s_o_file.Clear()
	self.s_fps.Clear()
	

#OnAccept()
    def OnAccept(self,e):
        fps = self.fps_preset[self.b_fps.GetCurrentSelection()]
        i_format = self.format_preset[self.b_i_format.GetSelection()]
        zeros = self.zeros_preset[self.b_zeros.GetCurrentSelection()]
        i_file=self.s_i_file.GetValue()
        o_dir=self.s_o_dir.GetValue()
        o_file=self.s_o_file.GetValue()

        if i_format != "tiff":
            num_zeros = int(zeros)
            offset = len(i_file) -4 - num_zeros
            i_fileXXX = i_file[:offset]+"%"+zeros+"d"+i_format 
        else:           
            num_zeros = int(zeros)
            offset = len(i_file) -5 - num_zeros
            i_fileXXX = i_file[:offset]+"%"+zeros+"d"+i_format

        if os.name=="posix":
             process_string = "avconv " + " -r "+fps +" -i " + i_fileXXX +" "+ o_dir +"/"+ o_file
             os.system(process_string)
        if os.name=="nt":
             process_string = "avconv " + " -r "+fps +" -i " + i_fileXXX +" "+ o_dir +"\\"+ o_file
             os.system("cd C:\MEDIA\videography\ffmpeg\bin")
	     os.system(process_string)
        
	

