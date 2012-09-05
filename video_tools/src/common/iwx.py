#! /usr/bin/env python
import wx

import cStringIO
import time
class iStaticText(wx.StaticText):

        
       
    def GetString(self):
       print "tbi" 

    def AddString(self,new_string):
	self.val = " "
        self.string = self.GetLabel()
	new_string= self.string+ " "+ new_string
        self.SetLabel(new_string)

        

    def Clear(self):
        is_filled =1
	try:
            self.string
        except AttributeError:

            is_filled=0
        if is_filled != 0:
                      
            self.SetLabel(self.string)
       
    def SetString(self,new_string):
        self.SetLabel(new_string)
        self.string = new_string
        

class iConsole(wx.TextCtrl):

    def out(self,string,mode = "default"):


        if mode == "default":
            self.SetForegroundColour('black')
        if mode == "error":
            self.SetForegroundColour('red')
        if mode == "good":
            self.SetForegroundColour('darkgreen')
        if mode == "bad":
            self.SetForegroundColour('orange')

        output="\n >> "+string
        self.AppendText( output )
           

class iForm(wx.Frame):

    def __init__(self,setup_list):
        self.num_cats= setup_list[1]
	self.names = setup_list[2]
        self.size = setup_list[0]
	wx.Frame.__init__(self, None)
        offset= (self.size[0]-20)/self.num_cats
	x_pos=10
        y_pos=10
        
        for i in self.names:
 
            # create iStaticText at postion
            self.s_name = iStaticText(self,-1,i,(x_pos,y_pos))
            
            # create button at postion
            # TODO: generate button names
            self.b_edit = wx.Button(self,wx.ID_ANY,"Edit",(x_pos,y_pos+20),(50,25),wx.BU_EXACTFIT)
            # create binding to button
            self.Bind(wx.EVT_BUTTON, self.OnEdit,self.b_edit)
            # create event
            y_pos= y_pos+offset 
        self.Show(True)

    def OnEdit(self,e):
        print "to be implemented"



class iList(wx.ListCtrl):
    def __init__(self,parent,i_size,i_pos,i_col_list):
#presets
        self.path_list = list()
        self.file_list = list()
        self.disp_list = list()
        self.LC = wx.ListCtrl(parent,size=i_size,pos= i_pos,style= wx.LC_REPORT | wx.BORDER_SUNKEN)
        
        col_num=0
        for col_name in i_col_list:
            self.LC.InsertColumn(col_num,col_name)
            col_num=col_num+1

         
        b_add=wx.Button(parent,wx.ID_ANY,"Add",(i_size[0]+20,40),(70,30),wx.BU_EXACTFIT)
        b_remove=wx.Button(parent,wx.ID_ANY,"Remove",(i_size[0]+20,80),(70,30),wx.BU_EXACTFIT)
        b_reset=wx.Button(parent,wx.ID_ANY,"Reset",(i_size[0]+20,120),(70,30),wx.BU_EXACTFIT)

        b_add.Bind(wx.EVT_BUTTON, self.OnAdd,b_add)
        b_remove.Bind(wx.EVT_BUTTON, self.OnRemove, b_remove)
        b_reset.Bind(wx.EVT_BUTTON, self.OnReset, b_reset)


# OnRemove()
    def OnRemove(self,e):
        indices = self.get_selected()
	
        # remove selected items
        for j in indices:
            self.LC.DeleteItem(j)
            self.file_list.pop(j)
            self.path_list.pop(j)

    def get_selected(self):
#get indices of selected items
        num_item = self.LC.GetItemCount()  

        i = 0
        indices = list()
        while i < num_item:
           a= self.LC.IsSelected(i)
           if a == True:
               indices.append(i)
           i = i+1
        return indices
        

# OnAdd()
    def OnAdd(self,e):

        dlg = wx.FileDialog(None,"Choose Files ",style =wx.FD_MULTIPLE )
        if dlg.ShowModal() == wx.ID_OK:
            self.file_list = dlg.GetFilenames()
            self.path_list = dlg.GetPaths()
            self.disp_list = dlg.GetFilenames()           
        dlg.Destroy()
#        self.seq_check(self.file_list)
        for f in self.disp_list:
            self.LC.InsertStringItem(0,f)    

    def seq_check(self,i):
        a = i[0]
        b = i[1]
        print a
        print b
        p = ""
#       check for pattern
        for c in b:
            chk = c in a
            if chk == True:

                p=p+"1"
            elif chk == False:

                p=p+ "0"
        

        i1= p.find("0")    
        i2= p.rfind("0")
        print p
        print i1
        print i2
        q = i1
        while True:
            q = q-1
            chk2 = "0" in a[q]
            if chk2 == True:
                continue
            elif chk2 ==False:
                break
            

        print a[0:q+1]
        print a[0:i1]
        start = a[q+1:i2]


#        start =int(start)
#        print start


            
# OnReset()    
    def OnReset(self,e):
        num_item = len(self.file_list)
        
        i=0
        while i < num_item:
            self.LC.DeleteItem(0)
            i=i+1
        self.file_list =[]
        self.path_list =[]
        self.disp_list=[]
# GetPaths()
    def GetPaths(self):
        indices=self.get_selected()
        out_list=()
        for i in indices:
            out_list.append(self.path_list[i])        
        return out_list
    
# GetNames()
    def GetNames(self):
        indices=self.get_selected()
        out_list=()
        for i in indices:
            out_list.append(self.path_list[i])        
        return out_list
        
        
        
        
        

        
        
    
        


        

