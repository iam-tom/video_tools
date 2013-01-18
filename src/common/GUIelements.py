#Module GUI ELEMENTS
#
#- elements of GUI such as buttons or checkboxes...V
import wx
import iwx
from  avtools import thumbnailer
import cStringIO
import imgutils
import utils
class iNavpanel(wx.Panel):
    def __init__(self,parent,steps):
        #default values
        wx.Panel.__init__(self,parent)
        self.ctr=0
        self.steps=steps
        self.layout()
        self.bindings()
    def layout(self):
        # layout
        bs1=wx.BoxSizer(wx.VERTICAL)
        bs12=wx.BoxSizer(wx.HORIZONTAL)
        bs11=wx.BoxSizer(wx.HORIZONTAL)
        fgs11=wx.FlexGridSizer(rows=1,cols=2)
        fgs11.SetFlexibleDirection(wx.HORIZONTAL)
        self.gauge=wx.Gauge(self,-1,range=self.steps)
        self.txt= wx.TextCtrl(self,-1)
        self.txt.SetEditable(False)
        self.updateTxt()



        #bs11.Add(self.gauge,wx.ALIGN_LEFT)
        #bs11.Add(self.txt,wx.ALIGN_RIGHT)
        fgs11.Add(self.gauge)
        fgs11.Add(self.txt  )


        self.forward=wx.Button(self,-1,"-->")
        self.back=wx.Button(self,-1,"<--")
        bs12.Add(self.back)
        bs12.Add(self.forward)

        #bs1.Add(bs11,wx.ALIGN_TOP)
        bs1.Add(fgs11)
        bs1.Add(bs12 )
        self.SetSizer(bs1)

    def bindings(self):
        #bindings
        self.forward.Bind(wx.EVT_BUTTON,self.OnForward)
        self.back.Bind(wx.EVT_BUTTON,self.OnBack)

    def OnForward(self,e):
        self.modifyCtr(1)
        self.gauge.SetValue(self.ctr)
        self.updateTxt()
        self.publishDirection(self.forward,1)


    def OnBack(self,e):
        self.modifyCtr(-1)
        self.gauge.SetValue(self.ctr)
        self.updateTxt()
        self.publishDirection(self.back,-1)

    def updateTxt(self):
        ctr_str=" "+ str(self.ctr)+utils.delimiter+str(self.steps)
        self.txt.SetValue(ctr_str)

    def modifyCtr(self,val):    
        if self.ctr + val < 0 or self.ctr +val >self.steps:
                print "[navbar] - invalid modification of ctr"
        else:
            self.ctr +=val

    def publishDirection(self,button,direction):
        evt=iwx.iEvent(iwx.EVT_INC_pub,1,direction)
        button.GetEventHandler().ProcessEvent(evt)

    def SetSteps(self,steps):
        self.steps = steps
        self.updateTxt()
        self.gauge.SetRange(steps)
        print self.steps

    def GetCtr(self):
        return self.ctr

class iChoice(wx.Choice):
#Default Resolution Choice element
    def __init__(self,parent,mode):
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
        index = wx.Choice.GetCurrentSelection(self)
	return self.choices_lookup[index]





class imgList (iwx.iList):
#iwx.iList with previewer and type check
    def __init__(self,parent,i_size):
        i_col_list = list()
        i_col_list.append("name")
        i_col_list.append("format")
        self.prev_config ={"pos":(i_size[0]+140,60),"parent":parent}
        super(imgList,self).__init__(parent,i_size,i_col_list)
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
            print "checked"
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
        self.config = {"format":".png","frame_size":"qvga", "i_path":"", "o_path":utils.folder_back+utils.folder_back+"tmp" }

        bmp  = self.get_bmp("data"+utils.delimiter+"prev_init.png")
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
        
        bmp = self.get_bmp(utils.folder_back+utils.folder_back+ self.canvas.SetBitmap(bmp))
        
    def OnReset(self,e):
        iwx.iList.OnReset(self,e)
        self.prev_init_state()


    def OnAdd(self,e):
        dlg = wx.FileDialog(None,"Choose Files ",style =wx.FD_MULTIPLE )
        if dlg.ShowModal() == wx.ID_OK:
            new_files = dlg.GetFilenames()
            new_paths = dlg.GetPaths()
            
            self.path_list = new_paths
            self.file_list =  new_files
            self.disp_list = new_files
        dlg.Destroy()
# When Sequence Detection is active
        if self.chkbx.IsChecked()==True:
            sc = imgutils.seq_compressor(set(self.path_list))
            groups= sc.get_groups()
            self.file_mapping=sc.get_mapping()
           
            meta = sc.get_meta()
            self.disp_list = list(groups)
            print self.disp_list
            i=0
            for f in self.disp_list:
                print "format = %s"% meta[i]["format"]
                self.LC.InsertStringItem(0,f)    
                self.LC.SetStringItem(0,1,meta[i]["format"])  
                i=i+1
        else:
            for f in self.disp_list:

                self.LC.InsertStringItem(0,f)
                
        
        
class iBrowse (wx.BoxSizer):

    def __init__(self,parent):
        self.topic = "Output Directory"
        self.btn_string = "Browse"
        self.parent = parent
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)
        self.setElements()

        
    def setElements(self):    
        self.t_browse =wx.TextCtrl(self.parent, -1, "", size=(150,30))
        self.b_browse=wx.Button(self.parent,-1,self.btn_string,size=wx.Size(70,30))
        self.b_browse.Bind(wx.EVT_BUTTON,self.OnBrowse,self.b_browse)
        self.Add(self.t_browse,wx.EXPAND)
        self.Add(self.b_browse,wx.ALIGN_TOP)
        
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
        
