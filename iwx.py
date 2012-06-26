#! /usr/bin/env python
import wx

class iStaticText(wx.StaticText):


    def GetString(self):
        self.string = self.GetLabel()
        print self.string

    def AddString(self,new_string):
	self.string = self.GetLabel()
	new_string= self.string+ " "+ new_string
        self.SetLabel(new_string)


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
           
