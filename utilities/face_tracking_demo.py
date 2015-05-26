import cv2
import numpy as np
import sys

sys.path.append("..")

import tools.Constants as c
import tools.face_detection as fd

def hist_curve(im, mask):
    
    bins = np.arange(16).reshape(16,1)
    h = np.zeros((300,16,3))
    
    col = (255,255,255)

    hist_item = cv2.calcHist([im],[0],mask,[16],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    pts = np.int32(np.column_stack((bins,hist)))
    cv2.polylines(h,[pts],False,col)
    y=np.flipud(h)
    print(y.shape)
    
    return y
    
def hist_lines(im, mask):
    
    bins = np.arange(16).reshape(16,1)
    h = np.zeros((300,16,3))
    hist_item = cv2.calcHist([im],[0],mask,[16],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    return y    

frame_1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_frame_1_pre_detection.bmp'
#frame_1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-imprese\ACTIVE-2014-12-12-slides\Immagini\Indicizzazione di contenuti video mediante riconoscimento dei volti e degli speaker\Frame_pre_tracking\0001461.bmp'
#frame_1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-imprese\ACTIVE-2014-12-12-slides\Immagini\Indicizzazione di contenuti video mediante riconoscimento dei volti e degli speaker\Frame_pre_tracking\0001488.bmp'

frame_2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_frame_2_pre_tracking.bmp'

save_path_1 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_frame_1_post_detection.png'

save_path_2 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_frame_2_back_projection.png'

save_path_3 = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_frame_3_post_tracking.png'

hist_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Tracking_example_histogram.png'

align_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Aligned'

show_results = True

params = {}

params[c.MIN_NEIGHBORS_KEY] = 5

result_dict =  fd.detect_faces_in_image(frame_1, align_path, params, show_results = False, return_always_faces = False)

#print(result_dict)

image = cv2.imread(frame_1, cv2.IMREAD_COLOR)

faces = result_dict[c.FACES_KEY]

face_dict = faces [0]
    
(x, y, w, h) = face_dict[c.BBOX_KEY]            

cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 3, 8, 0)

face = image[y:y+h, x:x+w]

#cv2.imwrite(save_path, face)
    
cv2.imshow('image',image)
cv2.waitKey(0)

#cv2.imwrite(save_path_1, image)

hsv_1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mask_1 = cv2.inRange(
hsv_1, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

hsv_roi = hsv_1[y:y+h, x:x+w]

mask_roi = mask_1[y:y+h, x:x+w]
    
hist = cv2.calcHist(
[hsv_roi], [0], mask_roi, [16], [0, 180])

cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
hist = hist.reshape(-1)

# Show histogram

curve = hist_lines(hsv_roi, mask_roi)
cv2.imshow('histogram',curve)
cv2.waitKey(0)

cv2.imwrite(hist_path, curve)

# Find tracking window in image 2

image2 = cv2.imread(frame_2, cv2.IMREAD_COLOR)

hsv_2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

mask_2 = cv2.inRange(hsv_2, 
np.array((0., 60., 32.)), np.array((180., 255., 255.)))

prob = cv2.calcBackProject(
[hsv_2], [0], hist, [0, 180], 1)

prob &= mask_2

cv2.imshow('back projection', prob)

cv2.waitKey(0)

#cv2.imwrite(save_path_2, prob)

term_crit = (cv2.TERM_CRITERIA_EPS 
| cv2.TERM_CRITERIA_COUNT, 10, 1)

track_box, track_window = cv2.CamShift(
prob, (x, y, w, h), term_crit)

track_x0 = track_window[0]
track_y0 = track_window[1]
track_w = track_window[2]
track_h = track_window[3]

cv2.rectangle(image2, (track_x0,track_y0), (track_x0+track_w, track_y0+track_h), (0,0,255), 3, 8, 0)
    
cv2.imshow('image',image2)
cv2.waitKey(0)

#cv2.imwrite(save_path_3, image2)
