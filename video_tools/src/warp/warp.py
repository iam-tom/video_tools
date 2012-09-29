from PIL import Image
from multiprocessing import Process
import utils
import transform
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
    def Run_pair(self,f0,f1):
        im0=f0 
        im1=f1
        im_ctr = 0
        out_file = self.o_path+"img_00000"
        for level in range(int(self.warp_frames)+1):
            alpha = float(level)/float(self.warp_frames)
            im_new=Image.blend(im0,im1,alpha)
            out_file_curr = out_file[0:len(out_file)-len(str(im_ctr))]+str(im_ctr)+self.o_type
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
            out_file = self.o_path+"img_00000"
            for level in range(int(self.warp_frames)+1):
                alpha = float(level)/float(self.warp_frames)
                im_new=Image.blend(im0,im1,alpha)

                
                
                out_file_curr = out_file[0:len(out_file)-len(str(im_ctr))]+str(im_ctr)+self.o_type
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
    
            out_file = self.o_path+"img_00000"
            for level in range(int(self.warp_frames)+1):
                alpha = float(level)/float(self.warp_frames)
                im_new=Image.blend(im0,im1,alpha)
                
                
                out_file_curr = out_file[0:len(out_file)-len(str(im_ctr))]+str(im_ctr)+self.o_type
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
    def set_input(self,f0,f1):
        self.f0 = f0
        self.f1 = f1
    ##
    # Start morphing process
    # @todo only work with PIL internally
    def Run(self):
        print"-----"
        print self.f0.pts()
        print"-----"
        print self.f1.pts()
        print"-----"
        est=transform.Affine_Fit(self.f0.pts(),self.f1.pts()) 
        t=est.Get_Trafo()
        T =  (t[0][3],t[1][3],t[2][3], t[0][4],t[1][4],t[2][4])
        img1=self.f1.pil_img()
        img0=self.f0.pil_img()
        img0.save("1.jpg")
        size=self.f0.size()
        self.img_morphed=img1.transform((size[0],size[1]),Image.AFFINE,T)
        self.img_morphed.save("2.jpg")
    def GetResult(self):
        return self.img_morphed

        
