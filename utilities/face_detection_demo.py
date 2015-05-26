# -*##- coding: utf-8 -*-
import cv2
import os
import sys

sys.path.append("..")

import tools.Constants as c
import tools.face_detection as fd

#resource_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face alignment\Frame_3.jpg'
#resource_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face recognition\Vittorio aligned.bmp'
#resource_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\lena.jpg'
#resource_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face alignment\Parameters_whole_image.jpg'
#resource_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face alignment\Parameters_whole_face.jpg'
resource_path = r'C:\Users\Maurizio\Dropbox\Screenshot\Screenshot 2015-05-25 17.38.27.png'

image = cv2.imread(resource_path, cv2.IMREAD_GRAYSCALE)

save_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face recognition\Vittorio aligned BW.png'

#cv2.imwrite(save_path, image)

align_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Aligned'

show_results = True

params = {}

params[c.MIN_NEIGHBORS_KEY] = 5

result_dict =  fd.detect_faces_in_image(resource_path, align_path, params, show_results = True, return_always_faces = False)

#print(result_dict)

image = cv2.imread(resource_path, cv2.IMREAD_COLOR)

faces = result_dict[c.FACES_KEY]

for face_dict in faces:
    
    (x, y, w, h) = face_dict[c.BBOX_KEY]            
    
    cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 3, 8, 0)
    
    face = image[y:y+h, x:x+w]
    
    cv2.imwrite(save_path, face)
    
cv2.imshow('image',image)
cv2.waitKey(0)

#cv2.imwrite(save_path, image)
