import shutil
import os
import random


class DBOrder():
        def __init__(self,dir_img,dir_db ):
                self._sep="---"
                self.dir_img=dir_img
                self.dir_db=dir_db
                if not self.dir_db.endswith("/"):
                        self.dir_db=self.dir_db+"/"    
                if not self.dir_img.endswith("/"):
                        self.dir_img=self.dir_img+"/"                         
        def prepare(self):
            pass
        
        def sort(self):
            all_image = os.listdir(self.dir_img)
            for im in all_image:
                if im.find(self._sep)>-1:
                    imsplit=im.split(self._sep)
                    if not os.path.exists( self.dir_db+"/"+str(imsplit[0]) ):
                                        os.makedirs( self.dir_db+"/"+str(imsplit[0]) )
 
                    shutil.copy(self.dir_img+im, self.dir_db+str(imsplit[0])+"/"+im)
                
if __name__ == "__main__":
    dbo=DBOrder("testimg", "ordered")
    dbo._sep="_I_"
    dbo.sort()