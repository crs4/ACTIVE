import cv2
import cv2.cv as cv
import numpy as np
import os
from Constants import *
from face_detection import detect_faces_in_image, get_cropped_face

resource = r'C:\Users\Maurizio\Documents\Video da YouTube\Non usati\Chirichella\#FIVBWomensWCH - Italia-Croazia 3-0- intervista a Cristina Chirichella.mp4'
images_path = r'C:\Users\Maurizio\Documents\Frame da video\fps originale\Chirichella'


capture = cv2.VideoCapture(resource)

frame_counter = 0

tracking = False

hist = None

track_window = None

model = None

prev_hist = None

for image_name in os.listdir(images_path):
    
    image_path = os.path.join(images_path, image_name)
    
    print image_path

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    vis = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    
    if(not(tracking)):
        
        det_res = detect_faces_in_image(image_path, None, True)
        
        err = det_res[ERROR_KEY]
        
        if err is None:
            
            faces = det_res[FACES_KEY]
            
            face_images = det_res[FACE_IMAGES_KEY]
            
            if(len(faces) == 1):
                
                bbox = faces[0]
                
                x0 = bbox[0]
                y0 = bbox[1]
                w = bbox[2]
                h = bbox[3]
                x1 = x0 + w
                y1 = y0 + h
                
                track_window = (x0, y0, w, h)
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
                hist = hist.reshape(-1)
                X = []
                X.append(np.asarray(face_images[0], dtype = np.uint8))
                c = [0]
                    
                model=cv2.createLBPHFaceRecognizer(
                LBP_RADIUS, 
                LBP_NEIGHBORS, 
                LBP_GRID_X, 
                LBP_GRID_Y)
                model.train(np.asarray(X), np.asarray(c))
                
                prev_hist = hist
                
                tracking = True
                
            else:
                
                print 'Warning! Zero or more than one face detected'
                
                cv2.imshow('frame', image)
    
                cv2.waitKey(0)
    
    else:
        
        prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.1 )
        track_box, track_window = cv2.CamShift(prob, track_window, term_crit)
        
        #print 'track_window = ', track_window
        
        x = track_window[0]
        y = track_window[1]
        w = track_window[2]
        h = track_window[3]
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3, 8, 0)
        
        track_face = image [y:(y+h), x:(x+w)]
        
        # Calculate difference between histograms
        
        bbox = faces[0]
                
        x0 = x
        y0 = y
        x1 = x0 + w
        y1 = y0 + h
        
        track_window = (x0, y0, w, h)
        hsv_roi = hsv[y0:y1, x0:x1]
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
        
        diff = cv2.compareHist(prev_hist, hist, cv.CV_COMP_CHISQR)
        
        print 'hist diff = ', diff
        
        prev_hist = hist
        
        cv2.imwrite(TMP_FRAME_FILE_PATH, track_face)
        
        sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
        
        face = get_cropped_face(TMP_FRAME_FILE_PATH, offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz, return_always_face = False)
        
        if face is not None:
        
            [lbl, conf] = model.predict(np.asarray(face, dtype = np.uint8))
            
            print "Predicted tag = %d (confidence=%.2f)" % (lbl, conf)
        
            cv2.imshow('image', image)
    
            cv2.waitKey(0)
            
            if(conf > STOP_TRACKING_THRESHOLD):
                
                tracking = True
                
            else:
                
                X = []
                X.append(np.asarray(face, dtype = np.uint8))
                c = [0]
                    
                model=cv2.createLBPHFaceRecognizer(
                LBP_RADIUS, 
                LBP_NEIGHBORS, 
                LBP_GRID_X, 
                LBP_GRID_Y)
                model.train(np.asarray(X), np.asarray(c))
