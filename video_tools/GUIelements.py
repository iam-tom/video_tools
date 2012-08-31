#Module GUI ELEMENTS
#
#- elements of GUI such as buttons or checkboxes...V
import wx
import iwx
from  av_tools import thumbnailer
import cStringIO

class iChoice(wx.Choice):
#Default Resolution Choice element
    def __init__(self,parent,in_pos,mode):
        #modes - to add new choice, just add new mode and check for it
        res_mode=mode in "res"
	if res_mode == True:
            self.choices_lookup=[(1280,720),(1920,1080),(640,480)]
            self.choices=["1280x720","1920x1080","640x480"] 
            heading = "Resolution"


        fps_mode=mode in "fps"
	if fps_mode == True:
            self.choices_lookup=[24,25,50]
            self.choices=["24fps","25fps","50fps"] 
            heading = "Framerate"


        #h=wx.StaticText(parent,wx.ID_ANY,heading)	
        super(iChoice,self).__init__(parent,wx.ID_ANY,choices=self.choices)
        #self.bs=wx.BoxSizer(wx.VERTICAL)       	
        #self.bs.Add(h,1,wx.EXPAND)
        #self.bs.Add(self,1,wx.EXPAND)
        #self.SetAutoLayout(True)
        #self.SetSizer(self.bs)
        #self.Layout()


    def GetChoice(self):
        index = wx.Choice.GetCurrentSelection()
	return self.choices_lookup(index)





class imgList (iwx.iList):
#iwx.iList with previewer and type check
    def __init__(self,parent,i_size,i_pos):
        i_col_list = list()
        i_col_list.append("name")
        i_col_list.append("format")
        self.prev_config ={"pos":(i_size[0]+140,60),"parent":parent}
        super(imgList,self).__init__(parent,i_size,i_pos,i_col_list)
        b_prev=wx.Button(parent,wx.ID_ANY,"Preview",(i_size[0]+20,160),(70,30),wx.BU_EXACTFIT)
        b_prev.Bind(wx.EVT_BUTTON, self.OnPrev,b_prev)
        self.T = thumbnailer()
        self.prev_init_state()
        wx.StaticText(parent,wx.ID_ANY,"Preview",pos=(i_size[0]+140,40))	

        self.chkbx=wx.CheckBox(parent,wx.ID_ANY," Img Seq",pos =(i_size[0]+20,200)) 



    def apply_file_mapping(self,indices,l):
        result=list()
        print indices
        print self.file_mapping
        for i in range(0,len(indices)):
            first  = self.file_mapping[self.disp_list[indices[i]]]
            if i<len(indices)-1 :
                last = self.file_mapping[self.disp_list[indices[i+1]]] 
            else:
                last = len(l)
            for i in range(first,last):
                result.append(l[i])    
            return result

    def GetPaths(self):
        indices=iwx.iList.get_selected(self)
        if self.chkbx.IsChecked()==True:
           out_list =  self.apply_file_mapping(indices,self.path_list)
        else:
           out_list = self.path_list    
        return out_list
    def GetNames(self):
        indices=iwx.iList.get_selected(self)
        if self.chkbx.IsChecked()==True:
           out_list =  self.apply_file_mapping(indices,self.file_list)
        else:
           out_list = self.file_list    
        print out_list    
        return out_list
                              
    def prev_init_state(self):
        self.config = {"format":".png","frame_size":"qvga", "i_path":"", "o_path":"/tmp/" }

        bmp  = self.get_bmp(".data/prev_init.png")
        self.canvas =wx.StaticBitmap(self.prev_config["parent"], -1, bmp,self.prev_config["pos"] )    

    def get_bmp(self,path):
        data = open(path, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        image = wx.ImageFromStream( stream )  

        bmp = wx.BitmapFromImage(image)
        return bmp
   
    def get_bmp_size(self,bmp):
        size = bmp.GetSize()
        return size
                
    def OnPrev(self,e):
        
        index = self.get_selected()
        self.config["i_path"] = self.path_list[index[0]]
        
        self.T.UpdateConfig(self.config)
        self.T.Run()
        
        bmp = self.get_bmp("/tmp/thb"+self.config["format"])
       
        self.canvas.SetBitmap( bmp)
        
    def OnReset(self,e):
        iwx.iList.OnReset(self,e)
        self.prev_init_state()
        
class iBrowse (wx.Panel):

    def __init__(self,parent,pos):
        self.topic = "Output Directory"
        self.btn_string = "Browse"
        self.parent = parent
        self.pos= pos
        self.setElements()

        
    def setElements(self):    
        self.t_browse =wx.TextCtrl(self.parent, -1, "", pos=self.pos,size=(150,30))
        self.b_browse=wx.Button(self.parent,wx.ID_ANY,self.btn_string,(self.pos[0]+150,self.pos[1]),(70,30),wx.BU_EXACTFIT)
        self.b_browse.Bind(wx.EVT_BUTTON,self.OnBrowse,self.b_browse)
        
    def OnBrowse(self,e):
        dir_dlg = wx.DirDialog(self.parent, "Choose a directory:",
                                 style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
            self.t_browse.AppendText(dir_dlg.GetPath())
    
    def SetText(self,topic,btn_string):
        self.topic = topic
        self.btn_string = btn_string
        self._setElements()
    
    def GetData(self):
        return self.t_browse.GetValue()
        
