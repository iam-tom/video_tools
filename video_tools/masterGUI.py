import wx
import imgGUI
import TimeLapseTools

class GUI (wx.Frame):

    def __init__(self,title,size):
        self.f = wx.Frame(None, title=title, size=size )
        self.f.Show()
    
    def spawn_imgGUI(self,size):
        in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/lapse0_002.jpg"
        self.p = imgGUI.GUI(self.f,size,in_path)
        b_accept=wx.Button(self.p,wx.ID_ANY,"OK",(size[0]+10,size[1]+10),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,self.OnAccept)        

    def OnAccept(self,e):
        boxes = self.p.GetBoxes()
        print boxes
        in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/"
        o = "/home/tom/lapse1"
        tlm= TimeLapseTools.tlm(in_path,o)
        tlm.computeBoxes((boxes[0].x,boxes[0].y),(boxes[1].x,boxes[1].y))
        frame_size=((boxes[1].x-boxes[0].x),(boxes[1].y-boxes[0].y))
        tlm.crop_scale_save(frame_size,frame_size)  

    
        


if __name__ == '__main__':
    app = wx.App(False)
    title="IMG GUI"
    size=(1920,1080)
    
    master = GUI(title,size)
    master.spawn_imgGUI((1080,720))   


    
    #p.PushEventHandler(MouseDownTracker(sys.stdout))

    app.MainLoop()

