import wx
import imgGUI
import TimeLapseTools

class GUI (wx.Frame):

    def __init__(self,title,size):
        self.f = wx.Frame(None, title=title, size=size )
        self.f.Show()
    
    def spawn_imgGUI(self,size,in_file,in_path,out_path):

        config = {in_path : in_path, in_file : in_file, out_path : out_path }
        
        self.p = imgGUI.GUI(self.f,size,in_file)
        b_accept=wx.Button(self.p,wx.ID_ANY,"OK",(size[0]+10,size[1]+10),(70,30),wx.BU_EXACTFIT)
        b_accept.Bind(wx.EVT_BUTTON,lambda  evt , config = config: self.OnAccept(evt,config))
       

    def OnAccept(self,e, config):
        boxes = self.p.GetBoxes()
        



        tlm= TimeLapseTools.tlm(config[in_path],config[out_path])
        a = ((boxes[0].x,boxes[0].y),(boxes[2].x,boxes[2].y))

        tlm.computeBoxes((boxes[0].x,boxes[0].y),(boxes[2].x,boxes[2].y))
        frame_size=((boxes[1].x-boxes[0].x),(boxes[1].y-boxes[0].y))
    
        raw_input("start processing")
        tlm.crop_scale_save(frame_size,frame_size)  

    
        


if __name__ == '__main__':
    app = wx.App(False)
    title="IMG GUI"
    size=(1920,1080)
    in_path = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/"
    in_file = "/host/MEDIA/photography/2012-04-20 SPAIN/sunrise/lapse0/lapse0_002.jpg"
    out_path = "/home/tom/lapse1"
    master = GUI(title,size)
    master.spawn_imgGUI((1080,720),in_file,in_path,out_path)   


    
    #p.PushEventHandler(MouseDownTracker(sys.stdout))

    app.MainLoop()

