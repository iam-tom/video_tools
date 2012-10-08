from project_config import path_config
pc=path_config("paths")
import wx
import tlmGUI
import GUIelements
import avtoolsGUI
import tlm

import subprocess
import iwx
import wdGUI
import warpGUI

from waitbar import iWaitbar
class GUI (wx.Frame):

    def __init__(self,title,config):
    
    
    #        calculate screen size etc
        ss_string = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True,stdout=subprocess.PIPE).communicate()[0]
        x_pos=ss_string.find('x')
        sw = int(ss_string[0:(x_pos)])
        sh = int(ss_string[x_pos+1:len(ss_string)])
        
        
        
        
        
        self.f = wx.Frame(None, title=title, size=(sw,sh) )
        
        splitter = wx.SplitterWindow(self.f,-1)
        
        self.p1 = wx.Panel(splitter,-1)
        self.p2 = wx.Panel(splitter,-1)
        
        splitter.SplitVertically(self.p1,self.p2)
        self.nb = wx.Notebook(self.p1)     
        


        
               
        config["size"] = (sw/2,sh)
        self.page1 = tlmGUI.tlmGUI(self.nb)
        #self.page3 = wdGUI.wdGUI(self.nb,config)
        self.page4 = warpGUI.warpGUI(self.nb) 
        self.nb.AddPage(self.page1, "TLM")
        #self.nb.AddPage(self.page3,"IMPORT")
        self.nb.AddPage(self.page4,"WARP")
        self.active_page = self.page1
        
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,self.OnTabChanged)
        
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        
#        graphical elements

        self.list = GUIelements.imgList(self.p2,(200,500))

        ok_b = wx.Button(self.p2,wx.ID_OK,"OK",(10,550),(80,80),wx.BU_EXACTFIT)
        ok_b.Bind(wx.EVT_BUTTON, self.OnOk)
        
        
        
        self.p1.SetSizer(sizer)
        self.p2.SetSizer(sizer)

        

        self.f.Show()
#/////////////  CALLBACKS
    def OnOk(self,e):
        names = self.list.GetNames()        
        paths = self.list.GetPaths()
        msg = list()
        if len(names) > 0 or len(paths) > 0:
            msg.append(paths)
            msg.append(names)
        
#            wx.Publisher().sendMessage("master.filesmsg",msg)
        
        self.active_page.SetInPath(msg)
#        self.page1.SetInPath(msg)
#        self.page3.SetInPath(msg)
        

    def OnTabChanged(self,event):
        self.active_page  = event.EventObject.GetChildren()[event.Selection]
        event.Skip()


        
                    
                    
    def OnPositions(self,msg):
        print msg.data
        
#        boxes = self.GetBoxes()
#        tlm= TimeLapseTools.tlm(config[in_path],config[out_path])
#        a = ((boxes[0].x,boxes[0].y),(boxes[2].x,boxes[2].y))

#        tlm.computeBoxes((boxes[0].x,boxes[0].y),(boxes[2].x,boxes[2].y))
#        frame_size=((boxes[1].x-boxes[0].x),(boxes[1].y-boxes[]
    
#        raw_input("start processing")
#        tlm.crop_scale_save(frame_size,frame_size)  

    
        


if __name__ == '__main__':
    app = wx.App(False)
    title="IMG GUI"
    size=(1920,1080)
    size2=(1280,720)
    in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/"
    in_file = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/lapse0_002.jpg"
#    in_file = "/home/tom/Pictures/Lebron-james_streetclothes.jpg"
    out_path = "/home/tom/lapse1"
    config = {"i_path": in_path, "i_file": in_file, "o_path": out_path , "size": size2 }        
    master = GUI(title,config)
#    master.spawn_imgGUI((1080,720),in_file,in_path,out_path)   


    
    #p.PushEventHandler(MouseDownTracker(sys.stdout))

    app.MainLoop()

