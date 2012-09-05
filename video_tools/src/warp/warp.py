from PIL import Image

class warper:

#Class is supposed to enable warping between a sequence of images

    def __init__(self):
        #initial values
        print "initialized"
        self.warp_frames=50.0
        self.in_path = list()
        self.in_path.append("seq_01.png")
        self.in_path.append("seq_02.png")
        self.in_path.append("seq_03.png")
        self.in_path.append("seq_04.png")
        self.in_path.append("seq_05.png")
        self.o_path="/share/goa-tz/evaluation_geometry_map/data/TF/screenshots/seq/"
        self.o_type=".png"
        self.config={"i_path":self.in_path,"o_path":self.o_path,"warp_frames":self.warp_frames,"o_type":self.o_type}
    def Update_config(self,config):
        self.config = config
        self.in_path = self.config["i_path"]
        self.o_path  = self.config["o_path"]
        self.warp_frames = self.config["warp_frames"]
        self.o_type = self.config["type"]
        
    
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
                alpha = level/self.warp_frames
                im_new=Image.blend(im0,im1,alpha)
                
                
                out_file_curr = out_file[0:len(out_file)-len(str(im_ctr))]+str(im_ctr)+self.o_type
                im_new.save(out_file_curr)
                im_ctr +=1
    
    

if __name__ == "__main__":
    a = warper()
    a.Run()
