#!/usr/bin/python

# commondialogs.py

import wx
import os, sys

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
      wx.Frame.__init__(self, parent, id, title)
      self.CreateStatusBar()
      menuBar = wx.MenuBar()
      menu = wx.Menu()
      #menu.Append(99,  "&Message Dialog", "Shows a Message Dialog")
      #menu.Append(100, "&Color Dialog", "Shows a Color Dialog")
      menu.Append(101, "&File Dialog", "Shows a File Dialog")
      #menu.Append(102, "&Page Setup Dialog", "Shows a Page Setup Dialog")
      #menu.Append(103, "&Font Dialog", "Shows a Font Dialog")
      menu.Append(104, "&Directory Dialog", "Shows a Directory Dialog")
      #menu.Append(105, "&SingleChoice Dialog", "Shows a SingleChoice Dialog")
      #menu.Append(106, "&TextEntry Dialog", "Shows a TextEntry Dialog")
      menuBar.Append(menu, "&Dialogs")
      self.SetMenuBar(menuBar)
      panel = wx.Panel(self, wx.ID_ANY)
 
      button = wx.Button(panel, id=wx.ID_ANY, label="Process")
      button.Bind(wx.EVT_BUTTON, self.onclick )
      
      
      #self.Bind(wx.EVT_BUTTON, self.onclick, id=102)

      self.Bind(wx.EVT_MENU, self.openfile, id=101)
      self.Bind(wx.EVT_MENU, self.opendir, id=104)

    def onclick(self,event):
        #os.system("echo [PS] ready to go to work\n")
        #os.system("echo [PS] selected dir:%s\n" % self.dir )
        #os.system("echo [PS] selected file:%s\n" % self.file )
 
        self.path=self.dir+self.file
        os.system("echo %s " % self.path)

        
    
    def openfile(self, event):
       dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
       if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                mypath = os.path.basename(path)
                self.file = mypath
                os.system("echo [PS] Path set to: %s" % mypath)
                self.SetStatusText("You selected: %s" % mypath)
       dlg.Destroy()
       
    def opendir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.SetStatusText('You selected: %s\n' % dlg.GetPath())
            self.dir = dlg.GetPath()
            os.system("echo [PS] Dir set to: %s" % self.dir)
        dlg.Destroy()
   
class MyApp(wx.App):
    def OnInit(self):
        myframe = MyFrame(None, -1, "commondialogs.py")
        myframe.CenterOnScreen()
        myframe.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
