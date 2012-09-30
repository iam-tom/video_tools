from PIL import Image
from multiprocessing import Process
import utils
import transform
import iwx
import imgutils
class warper:

#Class is supposed to enable warping between a sequence of images

    def __init__(self):
        #initial values
        print "initialized"
        self.warp_frames=50.0
        self.in_path = list()
        self.in_path.append("original.jpg")
        self.in_path.append("transformed.jpg")

        self.o_path="frames/"
        self.o_type=".jpg"
        self.config={"i_path":self.in_path,"o_path":self.o_path,"warp_frames":self.warp_frames,"o_type":self.o_type}
    def UpdateConfig(self,config):
        self.config = config
        self.in_path = self.config["i_path"]
        self.o_path  = self.config["o_path"]
        self.warp_frames = self.config["warp_frames"]
        self.o_type = self.config["o_type"]
    ##
    #   Mode with only 2 images 
    def RunPair(self,f0,f1,ctr=0):
        im0=f0 
        im1=f1
        im_ctr = ctr
        out_file = self.o_path+"img"
        for level in range(int(self.warp_frames)+1):
            alpha = float(level)/float(self.warp_frames)
            im_new=Image.blend(im0,im1,alpha)
            out_file_curr = out_file+utils.zero_str(4,im_ctr)+self.o_type
            im_new.save(out_file_curr)
            im_ctr +=1
               
    
    def Run(self):
        
        #load image and next image
        im_ctr = 0
        for i in range(len(self.in_path)-1):
    
            f0  = self.in_path[i]
            f1 = self.in_path[i+1]
    
            im0 = Image.open(f0)
            im1 = Image.open(f1)
    
            print "processing image %i "%i 
            out_file = self.o_path+"img"
            for level in range(int(self.warp_frames)+1):
                alpha = float(level)/float(self.warp_frames)
                im_new=Image.blend(im0,im1,alpha)

                out_file_curr = out_file+utils.zero_str(4,im_ctr)+self.o_type
                im_new.save(out_file_curr)
                im_ctr +=1
    def  Run_parallel(self):
         splitter = utils.split_seq(self.in_path,4)
         indices=splitter.get_indices()
         p1 = indices[1]
         p2 = indices[2]
         p3 = indices[3]

         paths_1=self.in_path[0:p1]
         paths_2=self.in_path[p1:p2]
         paths_3=self.in_path[p2:p3]
         paths_4=self.in_path[p3:-1]
         im_ctr1=0
         im_ctr2=p1*self.warp_frames
         im_ctr3=p2*self.warp_frames
         im_ctr4=p3*self.warp_frames
            



        Process(target=self.process_parallel,args=(paths_1,im_ctr1)).start()
         Process(target=self.process_parallel,args=(paths_2,im_ctr2)).start()
         Process(target=self.process_parallel,args=(paths_3,im_ctr3)).start()
         Process(target=self.process_parallel,args=(paths_4,im_ctr4)).start()

        
    def process_parallel(self,files,ctr):
        
        #load image and next image
        im_ctr = ctr
        for i in range(len(files)-1):
    
            f0 = files[i]
            f1 = files[i+1]
    
            im0 = Image.open(f0)
            im1 = Image.open(f1)
    
            out_file = self.o_path+"img",
            for level in range(int(self.warp_frames)+1):
                alpha = float(level)/float(self.warp_frames)
                im_new=Image.blend(im0,im1,alpha)
                
                out_file_curr = out_file+utils.zero_str(4,im_ctr)+self.o_type
                im_new.save(out_file_curr)
                im_ctr +=1
     

if __name__ == "__main__":
    a = warper()
    a.Run()



##
# Class handles transformation between two frames
class morpher():
    def __init__(self):
        print "[morpher] initialized"
    ##
    # Set input frames
    # @param f0 iwx.iFrame - start image
    # @param f1 iwx.iFrame - target image
    def SetInputFrames(self,f0,f1):
        self.f0 = f0
        self.f1 = f1

    ##
    # Calculate Transformation between two frames
    def GetTrafo(self):
        print"-----"
        print self.f0.pts()
        print"-----"
        print self.f1.pts()
        print"-----"
        est=transform.Affine_Fit(self.f0.pts(),self.f1.pts()) 
        t=est.Get_Trafo()
        return  (t[0][3],t[1][3],t[2][3], t[0][4],t[1][4],t[2][4])
    ##
    # Start morphing process
    # @todo only work with PIL internally
    def Run(self):
        T=self.GetTrafo()
        img1=self.f1.pil_img()
        self.transform(img1,T)
    ##
    # Apply transformation
    # @param img1 Frame to be transformed as PIL image
    # @param T transformation
    def Transform(self,img1,T):
        size=self.f0.size()
        self.img_morphed=img1.transform((size[0],size[1]),Image.AFFINE,T)
    ##
    # Get resulting morphed image
    # @param self Object pointer
    def GetResultImg(self):
        return self.img_morphed

##
# Function to process frame sequence.
# @param in_path List of input paths
# @param T transformation matrix
# @param out_path Output path where results are stored
def process_sequence(in_path,o_path,T): 
    tmp_path="/tmp/frames"
    o_type=".jpg"
    warp_frames=100
    utils.assert_dir(tmp_path)
    ctr= 0
    w=warper()
    config={"i_path":"","o_path":o_path,"warp_frames":warp_frames,"o_type":o_type}
    w.UpdateConfig(config)
    for f in range(len(in_path)-1):
        T_curr=T[ctr]
        if ctr ==0:
            
            #TODO: not right
            T_prev=(1,0,0,0, 0,1,0,0)
        else:
            T_prev=T[ctr-1]
        #TODO: make this work
        #T_use=imgutils.trafo_combine(T_curr,T_prev)
        if ctr == 0:
            f0=iwx.iFrame(in_path[ctr],ctr)
            f1=iwx.iFrame(in_path[ctr+1],ctr)
            img0 =f0.pil_img()
            img1 =f1.pil_img()
        else:
            img0 = mor
            f1=iwx.iFrame(in_path[ctr+1],ctr)
            img1=f1.pil_img()
        m=morpher()
        m.SetInputFrames(f0,f1)
        if ctr > 0:
            m.Transform(img1,T_prev)
            mor=m.GetResultImg()
            m.Transform(mor,T_curr)
        else:
            m.Transform(img1,T_curr)
        mor=m.GetResultImg()
        w.RunPair(img0,mor,ctr=ctr*warp_frames)
        ctr+=1
