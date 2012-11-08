#!/usr/bin/python

import project_config
pc=project_config.path_config("paths")
import wx
import iwx
import tlmGUI_new

if __name__=="__main__":
    print "TLM GUI TEST"
    app=wx.App(False)
    f=wx.Frame(None,-1,size=(900,1000))
    wg=tlmGUI_new.tlmGUI(f) 
    f.Show()
    app.MainLoop()
