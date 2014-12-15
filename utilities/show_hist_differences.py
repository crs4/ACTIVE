import cv2

import cv2.cv as cv

import matplotlib.pyplot as plt

import numpy as np

import os

import pickle

import sys

sys.path.append('..')

from tools.Constants import *

from tools.face_detection import detect_faces_in_image

from tools.Utils import get_shot_changes

glob_counter = 0

def calc_shot_changes():
    
    load_pickle_dump = False
    
    #images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Frames'
    
    #images_path = r'C:\Users\Maurizio\Documents\Frame da video\fps originale\Chirichella'
    
    #images_path = r'C:\Users\Maurizio\Documents\Frame da video\1 fps\Fic_02'
    
    #images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixTest1\Frames'
    
    #images_path = r'C:\Users\Maurizio\Documents\Face summarization\FPS_9_SCALE_FACTOR_0.5\Fic.02.mpg\Test'
    
    #images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Frames'
    
    images_path = r'C:\Users\Maurizio\Documents\Face summarization\YouTubeMix.mp4\Faces'
    
    #images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Faces'
    
    file_path = r'C:\Users\Maurizio\Documents\Face summarization\YouTubeMix.mp4\Diff_list'
    
    prev_hists = None
    
    diff_list = []
    im_counter = 0
    used_ims = []
    
    x_axis = []
    
    if(not(load_pickle_dump)):
    
        for image_name in os.listdir(images_path):
            
            print image_name
            
            image_path = os.path.join(images_path, image_name)
            
            print(image_path)
            
            #detection_result = detect_faces_in_image(
            #image_path, None, False)
            
            #if(detection_result is None):
                
                #continue
            
            #det_faces = detection_result[FACES_KEY]
            
            #if (len(det_faces) == 0):
                
                #continue
                
            #bbox = det_faces[0][BBOX_KEY]
            
            #x0 = bbox[0] + 5
            #y0 = bbox[1] + 5
            #w = bbox[2] - 10
            #h = bbox[3] - 10
            #x1 = x0 + w
            #y1 = y0 + h
            
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            
            #image = image[y0:y1, x0:x1]
            
            #cv2.imshow('face', image)
            
            #cv2.waitKey(0)
            
            #clothes_portion = image[270:540, 240:720]
            
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
            hists = []
            
            for ch in range(0, 1):
                
                hist = cv2.calcHist([hsv], [ch], mask, [256], [0, 255])
                
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                
                hist = hist.reshape(-1)
                
                hists.append(hist)
                
            if prev_hists is not None:
                
                tot_diff = 0
                
                for ch in range(0, 1):
                
                    diff = abs(cv2.compareHist(hists[ch], prev_hists[ch], cv.CV_COMP_CHISQR))
                    
                    tot_diff = tot_diff + diff
                
                diff_list.append(tot_diff)
                
                x_axis.append(image_name)
                
                used_ims.append(image_name)
            
            prev_hists = hists
            
            im_counter = im_counter + 1
            
        
        #mean = np.mean(diff_list)
        #std = np.std(diff_list)
        
        #threshold = mean + std
        
        #print 'mean = ', mean
        
        #print 'std = ', std
        
        #print 'threshold = ', threshold 
    
        with open(file_path, 'w') as f:
                        
            pickle.dump(diff_list, f)
            
        im_names_file_path = file_path + '_image_names'
        
        with open(im_names_file_path, 'w') as f:
            
            pickle.dump(used_ims, f)
    
    else:
        
        with open(file_path, 'r') as f:
                        
            diff_list = pickle.load(f)
    
    #mean = np.mean(diff_list)
    #std = np.std(diff_list)
    
    #if(True):
    ##if(std > mean):
        
        #threshold = mean + 1 * std

        #print 'mean = ', mean

        #print 'std = ', std

        #print 'threshold = ', threshold 
    
    #idxs = get_idxs_over_thresh(diff_list, 0, threshold)
    
    half_window_size = 9
    
    #idxs = get_shot_changes(diff_list, half_window_size, STD_MULTIPLIER_FRAME)
    
    print '\n\n### idxs ###\n\n'
    
    #min_dist = 25

    #idxs = merge_near_idxs(idxs, diff_list, min_dist)
    
    #print idxs
    
    #x_axis = range(0, len(diff_list))  
    
    #counter = 0
    #for x in x_axis:
		
		#x_axis[counter] = x_axis[counter] / 9.0
		
		#counter = counter + 1
    
    #print(diff_list)
    #print(x_axis)
    plt.plot(diff_list)
    #plt.xticks(range(0, len(diff_list)), x_axis)
    #plt.xlabel('s')
    plt.ylabel('Diff', fontsize = 20)
    #plt.title('Difference between neighbor frames')
    plt.show() 

def get_shot_changes_bad(diff_list, start_idx):
    '''
    Get frame counters  for shot changes
    
    :type diff_list: list
    :param diff_list: list with histogram differences
    
    :type start_idx: integer
    :param start_idx: start of this list in original list
    ''' 
    all_idxs = []
    
    # Do not consider segments whose duration is less than 1 second
    if(len(diff_list) < 25):
    #if(len(diff_list) == 0): 
        
        return all_idxs
    
    #print(diff_list)
    print('start_idx', start_idx)
    print 'len(list):', len(diff_list)
    
    #plt.plot(diff_list)
    #plt.show() 
    
    mean = np.mean(diff_list)
    std = np.std(diff_list)
    
    #if(True):
    if(std > mean):
        
        threshold = mean + 1 * std

        print 'mean = ', mean

        print 'std = ', std

        print 'threshold = ', threshold 
        
        #plt.plot(diff_list)
        #plt.show() 
        
        idxs = get_idxs_over_thresh(diff_list, start_idx, threshold)
        
        all_idxs.extend(idxs)
        
        sub_start_idx = 0
        
        for idx in idxs:
            
            print('idx', idx)
            
            sub_idx = idx - start_idx
            
            sub_list = diff_list[sub_start_idx:sub_idx]

            sub_sub_start_idx = start_idx + sub_start_idx

            sub_idxs = get_shot_changes(sub_list, sub_sub_start_idx)
            
            all_idxs.extend(sub_idxs)
            
            sub_start_idx = sub_idx + 1
            
        # Check last part of list
        if(len(idxs) > 0):
            sub_list = diff_list[sub_start_idx:]
    
            sub_sub_start_idx = start_idx + sub_start_idx
    
            sub_idxs = get_shot_changes(sub_list, sub_sub_start_idx)
                
            all_idxs.extend(sub_idxs)
    
    return all_idxs
    

def get_idxs_over_thresh(lst, start_idx, threshold):
    '''
    Get indexes of list items that are greater than given threshold
    '''
    
    idxs = []
    
    counter = start_idx
    
    for item in lst:
        
        if(item > threshold):
            
            #print 'idx = ', counter
            
            idxs.append(counter)
            
        counter = counter + 1
        
    print('idxs', idxs)   
        
    return idxs


def merge_near_idxs(idxs, diff_list, min_dist):
    '''
    Merge near indexes according to diff_list
    :type idxs: list
    :param idxs: list of indexes

    :type diff_list: list
    :param diff_list: list of histogram differences

    :type min_dist: integer
    :param min_dist: minimum distance between two indexes
    '''

    sorted_idxs = sorted(idxs)

    last_idx = len(diff_list) - 1

    item_deleted = True

    while(item_deleted):

        counter = 0
        prev = 0
        item_deleted = False
        
        for i in sorted_idxs:

            print i

            if(i < (prev + min_dist)):

                if((prev == 0) or (diff_list[i] <= diff_list[prev])):

                    del sorted_idxs[counter]
                    item_deleted = True
                    break

                else:

                    if(diff_list[i] > diff_list[prev]):

                        del sorted_idxs[counter - 1]
                        item_deleted = True
                        break

            elif(i > (last_idx - min_dist)):

                 del sorted_idxs[counter]
                 item_deleted = True
                 break
                 
            prev = i

            counter = counter + 1

    return sorted_idxs

#lst = [2, 2, 2, 1000, 3, 3, 3, 3, 3000, 2, 3, 2, 2, 300, 2]
#idxs = get_shot_changes(lst, 0)
#print('idxs', idxs)

calc_shot_changes()
