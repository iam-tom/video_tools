#! /usr/bin/env python
import wx

class iStaticText(wx.StaticText):


    def GetString(self):
        self.string = self.GetLabel()
        print self.string

    def AddString(self,new_string):
        self.value = new_string
	self.string = self.GetLabel()
	new_string= self.string+ " "+ new_string
        self.SetLabel(new_string)

    def getValue(self):
        is_set =1
        try:
            self.value
        except AttributeError:
            is_set = 0

        if is_set == 0:
            return ''
        else:
            return self.value


    def Clear(self):
        is_filled =1
	try:
            self.string
        except AttributeError:

            is_filled=0
        if is_filled != 0:
                      
            self.SetLabel(self.string)
       
    def SetString(self,new_string):
        self.SetLabel(new_string)
        self.string = new_string

class iConsole(wx.TextCtrl):

    def out(self,string,mode = "default"):


        if mode == "default":
            self.SetForegroundColour('black')
        if mode == "error":
            self.SetForegroundColour('red')
        if mode == "good":
            self.SetForegroundColour('darkgreen')
        if mode == "bad":
            self.SetForegroundColour('orange')

        output="\n >> "+string
        self.AppendText( output )
           

class iForm(wx.Frame):

    def __init__(self,setup_list):
        self.num_cats= setup_list[1]
	self.names = setup_list[2]
        self.size = setup_list[0]
	wx.Frame.__init__(self, None)
        offset= (self.size[0]-20)/self.num_cats
	x_pos=10
        y_pos=10
        
        for i in self.names:
 
            # create iStaticText at postion
            self.s_name = iStaticText(self,-1,i,(x_pos,y_pos))
            
            # create button at postion
            # TODO: generate button names
            self.b_edit = wx.Button(self,wx.ID_ANY,"Edit",(x_pos,y_pos+20),(50,25),wx.BU_EXACTFIT)
            # create binding to button
            self.Bind(wx.EVT_BUTTON, self.OnEdit,self.b_edit)
            # create event
            y_pos= y_pos+offset 
        self.Show(True)

    def OnEdit(self,e):
        print "to be implemented"
        



        
