#!/usr/bin/python

import project_config
pc=project_config.path_config("paths")
import wx
import iwx
import warpGUI

if __name__=="__main__":
    print "WARP GUI TEST"
    app=wx.App(False)
    f=wx.Frame(None,-1,size=(900,1000))
    wg=warpGUI.warpGUI(f) 
    f.Show()
    app.MainLoop()
