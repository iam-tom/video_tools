#!/usr/bin/env python

import itertools
import re
import PIL
import wx

class seq_compressor():
#class to compress the namestrings of image sequences
#
#usage:
# DATA =["x_01","x_02","x_03"]
# S = seq_compressor(DATA)
# compr_seq = S.get_groups

    def __init__(self,DATA):
        self.data = sorted(DATA)
        self.groups = set()
        self.meta = list()
        self.mapping=dict()
        self.last_index=0
# This algorithm only works if DATA is sorted.
#DATA = ["home/image_00101.png", "home/image_00102.png", "home/image_00103.png"]
    def get_groups(self):
        
        self. groups = [self.collapse_group(tuple(group)) \
                for key, group in itertools.groupby(enumerate(self.data),
                     lambda(index, name): index - int(self.extract_number(name)))]
        
        return self.groups

    def get_meta(self):
        if len(self.groups) >0:
            return self.meta 
    def get_mapping(self):
        if len(self.mapping)>0:
            return self.mapping 
    def extract_number(self,name):
         

         slash=name.rfind("/")
         dot = name.rfind(".")
         if dot >-1 and slash >-1: 
            skeleton =name[slash:dot]
         elif dot ==-1  and slash >-1:
            skeleton = name[slash:]
         elif dot >-1 and slash ==-1:
            skeleton = name[:dot]
         elif dot ==-1 and slash ==-1:
            skeleton = name 
         # Match the last number in the name and return it as a string,
         # including leading zeroes (that's important for formatting below).
         return re.findall(r"\d+$", skeleton)[0]

    def collapse_group(self,group):
         if len(group) == 1:
            self.last_index+=len(group)
            self.mapping[group[0][1]]=self.last_index    
            return group[0][1]  # Unique names collapse to themselves.
         else:    
             first = self.extract_number(group[0][1])  # Fetch range
             last = self. extract_number(group[-1][1])  # of this group.
             # Cheap way to compute the string length of the upper bound,
             # discarding leading zeroes.
             length = len(str(int(last)))
             dot = group[0][1].rfind(".")
              
             slash = group[0][1].rfind("/")
             
             # Now we have the length of the variable part of the names,
             # the rest is only formatting.
    
             #create mapping for group
             single_files =list()
             for file in group:
                 single_files.append(file)
             group_name = group[0][1][slash+1:dot-length]+"["+ first[-length:]+"-"+ last[-length:]+"]"
            # self.mapping[group_name]=single_files   
             self.mapping[group_name]=self.last_index   
             self.last_index+=len(group)
             #Set metadata of group
             num_items = len(group)
             seq_format= group[0][1][dot:len(group[0][1])]
             info ={"num_items":num_items,"format":seq_format}
             self.meta.append(info)
            
             return "%s[%s-%s]" % (group[0][1][slash+1:dot-length],
                 first[-length:], last[-length:])
    
def pil_to_image( pil, alpha=True):
    """ Method will convert PIL Image to wx.Image """
    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image


def image_to_pil( image):
    """ Method will convert wx.Image to PIL Image """
    pil = PIL.Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil 

##
# trafo multiplication    
def trafo_combine(a,b):
    q1=b[0]*a[0]+b[1]*a[3]
    q2=b[0]*a[1]+b[1]*a[4]
    q3=b[0]*a[2]+a[5]*b[1]+b[2]

    q4=b[3]*a[0]+b[4]*a[3]
    q5=a[4]*b[4]+b[3]*a[1]
    q6=b[3]*a[2]+b[4]*a[5]+b[5]
    
    r=tuple((q1,q2,q3,q4,q5,q6))        
    return r
