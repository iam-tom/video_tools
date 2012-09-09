import project_config
pr=project_config.path_config("paths")
import warp
import transform
from PIL import Image

import os

#imagees 9942-->9944
from_pt = ((2845,1668),(3369,1669),(3416,2324),(3242,1264))   # scaled x 2, rotated 45 degrees and translated
to_pt = ((2552,1624),(3087,1580),(3128,2301),(2958,1200)) # a 1x1 rectangle


#images 9979 --> 9971
from_pt = ((816,573),(1421,545),(1081,1054),(1188,441))   # scaled x 2, rotated 45 degrees and translated
to_pt = ((850,575),(1420,546),(1103,1030),(1200,443)) # a 1x1 rectangle




#from_pt = ((1,1),(1,2),(2,2),(2,1)) # a 1x1 rectangle
#to_pt = ((4,4),(6,6),(8,4),(6,2))   # scaled x 2, rotated 45 degrees and translated


tr=transform.Affine_Fit(from_pt,to_pt)

t= tr.Get_Trafo()
print tr.To_Str()
T =  (t[0][3],t[1][3],t[2][3], t[0][4],t[1][4],t[2][4])
#T =  (t[0][3],t[0][4],t[1][3], t[1][4],t[2][4],t[2][4])
im1=Image.open("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/01_2000.JPG")
im2=Image.open("/media/Data/MEDIA/photography/2012-08-30-Berlin/100CANON/02_2000.JPG")
im3 = im2.transform(im1.size,Image.AFFINE,T)
im3.save("transformed.jpg")
im1.save("original.jpg")

warper = warp.warper()
warper.Run()
