import cv2
import cv2.cv as cv
import numpy as np
import os
from Constants import *
from face_detection import detect_faces_in_image, get_cropped_face

use_video = False

resource = r'C:\Active\RawVideos\FicMix.mov'
images_path = r'C:\Users\Maurizio\Documents\Frame da video\fps originale\Chirichella'

capture = None

if(use_video):

    capture = cv2.VideoCapture(resource)

frame_counter = 0

tracking = False

hist = None

prev_hist = None

track_window = None

model = None

prev_hists = None

prev_prev_hists = None

diff_list = []

first_face = True

MIN_FRAMES_FROM_DETECTION = 10 # Dovranno essere calcolati dal tempo in 
#secondi (per esempio, 0,5 secondi) e dal bitrate

#for image_name in os.listdir(images_path):
    
    #image_path = os.path.join(images_path, image_name)
    
    #print image_path

    #image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
if use_video and (capture is None or not capture.isOpened()):

    error = 'Error in opening video file'

else:
    
    frames_from_detection = 0 
    
    ### Code to be used for video
    #while True:
    
        #ret, image = capture.read()
    
        #if(not(ret)):
            #break
            
    ### Code to be used for images
    for image_name in os.listdir(images_path):
        
        image_path = os.path.join(images_path, image_name)
        
        print image_path
    
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)        

    
        vis = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
        if(not(tracking)):
            
            frame_path = TMP_FRAME_FILE_PATH
            
            if(use_video):
                cv2.imwrite(TMP_FRAME_FILE_PATH, image)
                frame_path = TMP_FRAME_FILE_PATH
            else:
                frame_path = image_path
            
            det_res = detect_faces_in_image(frame_path, None, False)
            
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
                    prev_hist = hist
                    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
                    hist = hist.reshape(-1)
                    diff_list = []
                    
                    #tot_diff = 0
                    #prev_hists = []
                    #for ch in range(0,3):
                        #prev_hist = cv2.calcHist([hsv_roi],[ch],None,[256],[0,256])
                        ##cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
                        #prev_hists.append(prev_hist)
                        
                        #if(prev_prev_hists is not None):
                            ## Skip first face
                            #diff = cv2.compareHist(
                            #prev_prev_hists[ch], prev_hist, cv.CV_COMP_CHISQR)
                            #tot_diff = tot_diff + abs(diff)
                     
                    #if(prev_prev_hists is not None):
                        ## Not for first frame
                        #diff_list.append(tot_diff)
                        #print 'hist diff = ', tot_diff 
        
                    #prev_prev_hists = prev_hists
                    
                    #X = []
                    #X.append(np.asarray(face_images[0], dtype = np.uint8))
                    #c = [0]
                        
                    #model=cv2.createLBPHFaceRecognizer(
                    #LBP_RADIUS, 
                    #LBP_NEIGHBORS, 
                    #LBP_GRID_X, 
                    #LBP_GRID_Y)
                    #model.train(np.asarray(X), np.asarray(c))
                    
                    frames_from_detection = 0
                    tracking = True
                    
                else:
                    
                    print 'Warning! Zero or more than one face detected'
                    
                    #cv2.imshow('frame', image)
        
                    #cv2.waitKey(0)
        
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
            
            #bbox = faces[0]
                    
            x0 = x
            y0 = y
            x1 = x0 + w
            y1 = y0 + h
            
            track_window = (x0, y0, w, h)
            hsv_roi = hsv[y0:y1, x0:x1]
            mask_roi = mask[y0:y1, x0:x1]
            new_hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
            #cv2.normalize(new_hist, new_hist, 0, 255, cv2.NORM_MINMAX);
            new_hist = new_hist.reshape(-1)
            diff = abs(cv2.compareHist(new_hist, prev_hist, cv.CV_COMP_CHISQR))
            
            prev_hist = new_hist
            
            print 'hist diff = ', diff
            
            #tot_diff = 0
            #hists = []
            #for ch in range(0,3):
                #new_hist = cv2.calcHist([hsv_roi],[ch],None,[256],[0,256])
                ##cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
                #hists.append(new_hist)
                #if(prev_hists is not None):
                    ## Skip first face
                    #diff = cv2.compareHist(
                    #prev_hists[ch], new_hist, cv.CV_COMP_CHISQR)
                    #tot_diff = tot_diff + abs(diff)
            
            frames_from_detection = frames_from_detection + 1
            
            if(frames_from_detection > MIN_FRAMES_FROM_DETECTION):
                
                mean = np.mean(diff_list)
                std = np.std(diff_list)
                
                threshold = mean + 2 * std
                
                print 'threshold = ', threshold
                
                if(diff > threshold):
                    
                    tracking = False
                    
                    cv2.imshow('image', image)
        
                    cv2.waitKey(0)   

            
                #prev_hists = hists
               

               
            if(tracking):
                    
                diff_list.append(diff)
            
            #cv2.imwrite(TMP_FRAME_FILE_PATH, track_face)
            
            #sz = (CROPPED_FACE_WIDTH,CROPPED_FACE_HEIGHT)
            
            #face = get_cropped_face(TMP_FRAME_FILE_PATH, offset_pct = (OFFSET_PCT_X,OFFSET_PCT_Y), dest_size = sz, return_always_face = False)
            
            #if face is not None:
            
                #[lbl, conf] = model.predict(np.asarray(face, dtype = np.uint8))
                
                #print "Predicted tag = %d (confidence=%.2f)" % (lbl, conf)
            
                #cv2.imshow('image', image)
        
                #cv2.waitKey(0)
                
                #if(conf > STOP_TRACKING_THRESHOLD):
                    
                    #tracking = True
                    
                #else:
                    
                    #X = []
                    #X.append(np.asarray(face, dtype = np.uint8))
                    #c = [0]
                        
                    #model=cv2.createLBPHFaceRecognizer(
                    #LBP_RADIUS, 
                    #LBP_NEIGHBORS, 
                    #LBP_GRID_X, 
                    #LBP_GRID_Y)
                    #model.train(np.asarray(X), np.asarray(c))

mean = np.mean(diff_list)
    
print 'mean = ', mean

std = np.std(diff_list)

print 'std = ', std 
