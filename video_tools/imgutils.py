#!/usr/bin/env python

import itertools
import re
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
             return group[0][1]  # Unique names collapse to themselves.
         first = self.extract_number(group[0][1])  # Fetch range
         last = self. extract_number(group[-1][1])  # of this group.
         # Cheap way to compute the string length of the upper bound,
         # discarding leading zeroes.
         length = len(str(int(last)))
         dot = group[0][1].rfind(".")
          
         slash = group[0][1].rfind("/")
         
         # Now we have the length of the variable part of the names,
         # the rest is only formatting.


         #Set metadata of group
         num_items = len(group)
         seq_format= group[0][1][dot:len(group[0][1])]
         info ={"num_items":num_items,"format":seq_format}
         self.meta.append(info)
        
         return "%s[%s-%s]" % (group[0][1][slash+1:dot-length],
             first[-length:], last[-length:])


