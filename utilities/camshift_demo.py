import numpy as np
import cv2
from time import sleep

cap = cv2.VideoCapture('C:\Users\Maurizio\Documents\Video da YouTube\Datome_Gigi\TrainingTest3.mp4')

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
c, r, w, h = 185,119,200,200  # simply hardcoded the values
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[16],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
roi_hist = roi_hist.reshape(-1)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()
    pts = cv2.rectangle(frame, (track_window[0], track_window[1]), (track_window[0]+track_window[2], track_window[1]+track_window[3]), (0, 0, 255) )
    cv2.imshow('img2', frame)

    cv2.waitKey(0)

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        sub_mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        dst &= sub_mask

        cv2.imshow('img2', dst)
        cv2.waitKey(0)
	
        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.rectangle(frame, (track_window[0], track_window[1]), (track_window[0]+track_window[2], track_window[1]+track_window[3]), (0, 0, 255) )
        #pts = np.int0(pts)
        #img2 = cv2.polylines(frame,[pts],True, 255,2)
        cv2.imshow('img2', frame)
        cv2.waitKey(0)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",frame)

    else:
        break


cv2.destroyAllWindows()
cap.release()
