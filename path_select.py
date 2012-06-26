#!/usr/bin/python



import wx
import os, sys

class path_select(wx.Frame):
    def __init__(self, parent, id, title):
        dlg = wx.FileDialog(self,"Select path",os.getcwd(), "", "*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlf.GetPath()
            mypath = os.path.basename(path)
            #self.SetStatusText("selected %s\n"% str(data.GetColour().Get()))
            dlg.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        path_select = MyApp(None, -1, "path_select.py")
        path_select.CenterOnScreen()
        path_select.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
