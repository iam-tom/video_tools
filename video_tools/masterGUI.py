import wx
import imgGUI
import avconvGUI
import TimeLapseTools
from wx.lib.pubsub import Publisher
import subprocess

class GUI (wx.Frame):

    def __init__(self,title,config):
    
    
    #        calculate screen size etc
        ss_string = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True,stdout=subprocess.PIPE).communicate()[0]
        x_pos=ss_string.find('x')
        sw = int(ss_string[0:(x_pos)])
        sh = int(ss_string[x_pos+1:len(ss_string)])
        
        
        
        self.f = wx.Frame(None, title=title, size=(sw,sh) )
        self.f.Show()
        
        splitter = wx.SplitterWindow(self.f,-1)
        
        self.p1 = wx.Panel(splitter,-1)
        self.p2 = wx.Panel(splitter,-1)
        
        splitter.SplitVertically(self.p1,self.p2)
        self.nb = wx.Notebook(self.p1)     
        


        
               
        
        page1 = imgGUI.GUI(self.nb,config)
        page2 = avconvGUI.GUI(self.nb)
        self.nb.AddPage(page1, "TLM")
        self.nb.AddPage(page2, "AVCONV")
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.p1.SetSizer(sizer)
        

        #page1.setNewState(config["i_file"])
        
                
    def spawn_imgGUI(self,size,in_file,in_path,out_path):

        config = {"i_path": in_path, "i_file": in_file, "o_path": out_path , "size": size }        
        self.imgGUI = imgGUI.GUI(self.f,config)
        Publisher().subscribe(self.positions,("imgGUI.positions"))
                    
                    
    def positions(self,msg):
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
    out_path = "/home/tom/lapse1"
    config = {"i_path": in_path, "i_file": in_file, "o_path": out_path , "size": size2 }        
    master = GUI(title,config)
#    master.spawn_imgGUI((1080,720),in_file,in_path,out_path)   


    
    #p.PushEventHandler(MouseDownTracker(sys.stdout))

    app.MainLoop()

