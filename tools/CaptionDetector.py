import cv2
import cv2.cv as cv
import os
from caption_recognition import get_tag_from_image

####    TEST ONLY      ####

use_all_images = False

if (use_all_images):
   
    folder = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina - Training set da testo\Fic.06\Training_set_ordered\Simonazzi_Aurelio'
    
    folder_list = folder.split('\\')
    annotated_label = folder_list[len(folder_list) - 1]
    
    print 'annotated_label:', annotated_label
    
    true_pos_nr = 0 
    
    min_eq_letters_true_pos = 1000
    max_eq_letters_false_pos = -1
    tot_letters_max_false_pos = 0
    sum_eq_letters_true_pos = 0
    
    for image in os.listdir(folder):
        
        image_complete_path = folder + os.sep + image;
        
        #print(image_complete_path)
        
        result_dict = get_tag_from_image(image_complete_path)
        assigned_label = result_dict[ASSIGNED_LABEL_KEY]
        
        eq_letters_nr = result_dict[EQ_LETTERS_NR_KEY]
        
        tot_letters_nr = result_dict[TOT_LETTERS_NR_KEY]
        
        if(assigned_label == annotated_label):
            
            true_pos_nr = true_pos_nr + 1
            
            sum_eq_letters_true_pos = sum_eq_letters_true_pos + eq_letters_nr
            
            if(eq_letters_nr < min_eq_letters_true_pos):
                
                min_eq_letters_true_pos = eq_letters_nr
                
        else:
            
            if(eq_letters_nr > max_eq_letters_false_pos):
                
                max_eq_letters_false_pos = eq_letters_nr
                tot_letters_max_false_pos = tot_letters_nr        
                
    print 'true positives:', true_pos_nr
    
    if(USE_LEVENSHTEIN):
        if(true_pos_nr > 0):
            print 'mean Levenshtein ratio in true positives:', float(sum_eq_letters_true_pos) / true_pos_nr
            print 'min Levenshtein ratio in true positives:', min_eq_letters_true_pos
        print 'max Levenshtein ratio in false positives:', max_eq_letters_false_pos
        print 'max possible Levenshtein ratio in false positive with max Levenshtein ratio:', tot_letters_max_false_pos
    
    else:
        
        if(true_pos_nr > 0):
            print 'mean number of equal letters in true positives:', float(sum_eq_letters_true_pos) / true_pos_nr
            print 'min number of equal letters in true positives:', min_eq_letters_true_pos
        print 'max number of equal letters in false positives:', max_eq_letters_false_pos
        print 'tot number of letters in false positive with max number of equal letters:', tot_letters_max_false_pos    
        
else:
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Caption detection\Baldaccini.bmp'
    image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video Videolina\Originali\BaldacciniDOcchiChiusi.jpg'
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video YouTube\Originali\Fisichella_Giancarlo.jpg'
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video Videolina\Originali\CabrasTest1.jpg'
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\Videolina - Training set da testo\Fic.02\Training_set_ordered\Caredda_Giorgio\frame1216.jpg'
    
    image_path = r'C:\Users\Maurizio\Documents\File di test\Caption recognition\Caption_orig.jpg'
    #fm = FaceModelsLBP()
    
    gray_im = cv2.imread(image_path, cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)
    get_tag_from_image(gray_im)
    
