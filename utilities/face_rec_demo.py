import cv2
import numpy as np
import sys

sys.path.append("..")

import tools.Constants as c
import tools.face_detection as fd

def hist_curve(hist_item):
    h = np.zeros((20,len(hist_item),1))
    col = (255,255,255)
    bins = np.arange(len(hist_item)).reshape(len(hist_item),1)
    hist=np.int32(np.around(hist_item*100))
    pts = np.int32(np.column_stack((bins,hist)))
    cv2.polylines(h,[pts],False,col)
    y=np.flipud(h)
    print(y.shape)
    
    return y
    
def hist_lines(hist_item):
    h = np.zeros((300,len(hist_item),1))
    bins = np.arange(len(hist_item)).reshape(len(hist_item),1)
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    return y  

image_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face recognition\Vittorio aligned BW.png'

save_path = r'C:\Users\Maurizio\Google Drive\Progetto ACTIVE\ACTIVE-Incontro-universita\Immagini\Algoritmi e tecniche di face detection  tracking  recognition\Face recognition\Histograms.png'

face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

model = cv2.createLBPHFaceRecognizer(1, 8, 4, 8)
        
X, y = [], []

X.append(np.asarray(face, dtype = np.uint8))
y.append(0)
        
model.train(np.asarray(X), np.asarray(y))

model_hists = model.getMatVector("histograms")

hist = model_hists[0][0]

print(max(hist))

# Show histogram

curve = hist_curve(hist)
cv2.imshow('histogram',curve)
cv2.waitKey(0)

line = hist_lines(hist)
cv2.imshow('histogram',line)
cv2.waitKey(0)

cv2.imwrite(save_path, line)
