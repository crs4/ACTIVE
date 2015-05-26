import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

frame_path = r'C:\Users\Maurizio\Pictures\135.bmp'
frame_path = r'C:\Users\Maurizio\Pictures\40.bmp'
#frame_path = r'C:\Users\Maurizio\Documents\Frame da video\Per face detection\MONITOR072011\I\MONITOR072011_I_006.jpg'
#frame_path = r'C:\Users\Maurizio\Documents\Frame da video\Per face detection\MONITOR072011\I\MONITOR072011_I_042.jpg'
#frame_path = r'C:\Users\Maurizio\Pictures\frame_monitor.bmp'
#frame_path = r'C:\Users\Maurizio\Documents\Frame da video\0.1 fps - selezionati\fic.02\frame0019.jpg'
frame_path = r'F:\Key frames\0000048.png'
#frame_path = r'C:\Users\Maurizio\Documents\Face summarization\Test\Soglia variabile\TEST ID 19\fic.02.mpg\People clustering\Key frames\0000000.png'

clothing_width_pct = 2.0

clothing_height_pct = 1.0

classifier_file = r'C:\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_alt2.xml'

rgb_image = cv2.imread(frame_path, cv2.IMREAD_COLOR)

image = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

haar_scale = 1.1

min_neighbors = 5

haar_flags = 0

min_size = (20, 20)

face_cascade_classifier = cv2.CascadeClassifier(classifier_file)

faces = face_cascade_classifier.detectMultiScale(
image, haar_scale, min_neighbors, haar_flags, min_size)

for (x, y, w, h) in faces:
    
    cv2.rectangle(rgb_image, (x, y), (x + w, y + h), (255, 255, 255), 4)
    
    cl_w = int(clothing_width_pct * w)
    
    cl_h = int(clothing_height_pct * h)
    
    cl_x = int(x + w/2.0 - cl_w/2.0)
    
    cl_y = int(y + h)
    
    print('cl_y + cl_h', cl_y + cl_h)
    
    height, width, depth = rgb_image.shape
    
    print('image height', height)
    
    cv2.rectangle(rgb_image, (cl_x, cl_y), (cl_x + cl_w, cl_y + cl_h), (255, 255, 255), 4)
    
    roi = rgb_image[cl_y:cl_y + cl_h, cl_x:cl_x + cl_w]
    
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(roi_hsv, 
    np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    
    good_pixels = cv2.countNonZero(mask)
    
    print('good pixels', good_pixels) 
    
    mask_size = (cl_h * cl_w)
    
    print('mask size', mask_size) 
    
    pct = float(good_pixels) / mask_size
    
    print('pct', pct)
    
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    
cv2.imshow('image', rgb_image)
cv2.waitKey(0)

#out_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\Immagini\Clothing recognition\Chothing_example_1_no_text.png'

#cv2.imwrite(out_path, rgb_image)

#img = mpimg.imread(out_path)
#plt.imshow(img)


