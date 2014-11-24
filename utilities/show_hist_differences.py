import cv2

import cv2.cv as cv

import matplotlib.pyplot as plt

import numpy as np

import os


#images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMix\Frames'

#images_path = r'C:\Users\Maurizio\Documents\Frame da video\fps originale\Chirichella'

#images_path = r'C:\Users\Maurizio\Documents\Frame da video\1 fps\Fic_02'

images_path = r'C:\Users\Maurizio\Documents\Face summarization\FicMixTest1\Frames'

prev_hists = None

diff_list = []

for image_name in os.listdir(images_path):
    
    print image_name
    
    image_path = os.path.join(images_path, image_name)
    
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    #clothes_portion = image[270:540, 240:720]
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

    hists = []
    
    for ch in range(0, 3):
        
        hist = cv2.calcHist([hsv], [ch], mask, [256], [0, 255])
        
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        
        hist = hist.reshape(-1)
        
        hists.append(hist)
        
    if prev_hists is not None:
        
        tot_diff = 0
        
        for ch in range(0, 3):
        
            diff = abs(cv2.compareHist(hists[ch], prev_hists[ch], cv.CV_COMP_CHISQR))
            
            tot_diff = tot_diff + diff
        
        diff_list.append(tot_diff)
    
    prev_hists = hists
    

mean = np.mean(diff_list)
std = np.std(diff_list)

threshold = mean + std

print 'mean = ', mean

print 'std = ', std

print 'threshold = ', threshold 

plt.plot(diff_list)
plt.show() 
