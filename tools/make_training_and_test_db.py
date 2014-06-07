import shutil
import os
import random
from FaceModelsLBP import FaceModelsLBP

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

    training_input_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Training_set'
    training_output_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Training_set_ordered'

    images_dirs = os.listdir(training_output_path);

    # Deleting files in output path
    for images_dir in images_dirs:
        images_dir_complete_path = training_output_path + os.sep + images_dir;
        shutil.rmtree(images_dir_complete_path)

    # Training db creation
    dbo=DBOrder(training_input_path, training_output_path)
    dbo._sep=" -- "
    dbo.sort()

    fm = FaceModelsLBP(force_db_creation = True);

    test_input_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Test_set_only_faces'
    test_output_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Test_set_only_faces_ordered'

    images_dirs = os.listdir(test_output_path);

    # Deleting files in output path
    for images_dir in images_dirs:
        images_dir_complete_path = test_output_path + os.sep + images_dir;
        shutil.rmtree(images_dir_complete_path)    

    # Test db creation
    dbo=DBOrder(test_input_path, test_output_path)
    dbo._sep=" -- "
    dbo.sort()

    test_input_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Test_set_whole_images'
    test_output_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina\Dataset_10\Test_set_whole_images_ordered'

    images_dirs = os.listdir(test_output_path);

    # Deleting files in output path
    for images_dir in images_dirs:
        images_dir_complete_path = test_output_path + os.sep + images_dir;
        shutil.rmtree(images_dir_complete_path)    

    # Test db creation
    dbo=DBOrder(test_input_path, test_output_path)
    dbo._sep=" -- "
    dbo.sort()
