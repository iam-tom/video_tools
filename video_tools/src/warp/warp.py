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
    #   Run blending for two images
    #   @param f0 Start frame
    #   @param f1 End frame
    #   @param ctr Image numbering start counter
    def process_imgs(self,f0,f1,ctr=0):
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
               
   ##
   # Run warping process with specified configuration 
    def Run(self):
        
        #load image and next image
        im_ctr = 0
        for i in range(len(self.in_path)-1):
    
            p0  = self.in_path[i]
            p1 = self.in_path[i+1]
    
            im0 = Image.open(p0)
            im1 = Image.open(p1)

            self.process_imgs(im0,im1,ctr=im_ctr*self.warp_frames)
            im_ctr+=1

   ##
   # Run warping process with specified configuration with multiprocessing
   # @param num_proc Number of processes that are spawned
    
    def  Run_parallel(self,num_proc=4):
         splitter = utils.split_seq(self.in_path,num_proc)
         indices=splitter.get_indices()

         for i in range(num_proc-1):
             if i==0:
                p0 =0
             else:
                p0=indices[i]   
                p1=indices[i+1]    

         paths=self.in_path[p0:p1]
         im0=Image.open(self.in_path[p0])
         im1=Image.open(self.in_path[p1])
         im_ctr=p0*warp_frames
         Process(target=self.process_imgs,args=(paths,im_ctr)).start()


if __name__ == "__main__":
    a = warper()
    a.Run()



##
# Class handles transformation between two frames
class morpher():
    def __init__(self):

        self.T=0
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
    def calc_trafo(self):
        print"-----"
        print self.f0.pts()
        print"-----"
        print self.f1.pts()
        print"-----"
        est=transform.Affine_Fit(self.f0.pts(),self.f1.pts()) 
        t=est.Get_Trafo()
        self.T= (t[0][3],t[1][3],t[2][3], t[0][4],t[1][4],t[2][4])
    ##
    # Start morphing process
    # @todo only work with PIL internally
    def Run(self,T=0,trafo_only=False):
        if T ==0:
            self.calc_trafo()
        else:
            self.T=T
        img1=self.f1.pil_img()
        if trafo_only==False:
            self.transform(img1,self.T)
    ##
    # Apply transformation
    # @param img1 Frame to be transformed as PIL image
    # @param T transformation
    def transform(self,img1,T):
        size=self.f0.size()
        self.img_morphed=img1.transform((size[0],size[1]),Image.AFFINE,T)
    ##
    # Get resulting morphed image
    # @param self Object pointer
    def GetImgM(self):
        return self.img_morphed
    
    ##
    # Get transformation
    def GetTrafo(self):
        if self.T==0:
            print "execute Run() first"
        return self.T
    ##
    # Save resultant image
    def SaveImgM(self,o_path):        
        self.img_morphed.save(o_path+".jpg")

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
            m.Run(T_prev)
            mor=iwx.iFrame(m.GetImgM())
            m.SetInputFrames(f0,mor)
            m.Run(T_curr)
        else:
            m.Run(T_curr)
        mor=m.GetImgM()
        w.process_images(img0,mor,ctr=ctr*warp_frames)
        ctr+=1

#TODO: - make morphing during GUI activity work
        #- warping afterwards  / is parallelity even possible
