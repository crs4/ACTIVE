import cv2
import cv2.cv as cv
import numpy as np
import tesseract
from Constants import LABEL_SEP
from FaceModelsLBP import FaceModelsLBP
from os import listdir

LETT_MARGIN = 2

MIN_CHAR_HEIGHT = 5

MAX_CHAR_HEIGHT_PCT = 0.2

MAX_CHAR_WIDTH_PCT = 0.2

KERNEL_MAX_SIZE = 5

MIN_HEIGHT_FOR_OCR = 100

I_MIN_SATURATION = 0.75
I_MAX_WIDTH_TO_HEIGHT_RATIO = 0.4

MAX_BBOX_DIFF = 10

PELS_TO_TEXT_SIZE_RATIO = 25.7

USE_METHOD_2 = True

def get_tag_from_image(image_path, face_models):
    
    # Tesseract init
    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
    api.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)
    
    rgb_im = cv2.imread(image_path) # TEST ONLY
    
    gray_im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE);
    
    im_height, im_width = gray_im.shape
    #print(im_height)
    
    # Convert grayscale image to black and white image
    flags = cv2.THRESH_BINARY | cv2.THRESH_OTSU
    th, bw_im = cv2.threshold(gray_im, 128, 255, flags)
    
    # Find contours in image
    mode = cv2.RETR_TREE
    method = cv2.CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(bw_im, mode, method)
    
    # Order contours from left to right
    bbox_xs = []
    bboxs = []
    contour_idx = 0
    
    for contour in contours:
        
        bbox = cv2.boundingRect(contour)
        x1 = bbox[0]
        y1 = bbox [1]
        x2 = x1 + bbox[2]
        y2 = y1 + bbox[3]
        
        bbox_xs.append(x1)
        bboxs.append(bbox)
        
    idxs = [i[0] for i in sorted(enumerate(bbox_xs), key=lambda x:x[1])]
    
    useful_contour_counter = 0
    all_letters = []
    all_letters_str = ''
    
    ord_bboxs = []
    ord_contour_idxs = []
    
    for idx in idxs:
        
        bbox = bboxs[idx]
        x1 = bbox[0]
        y1 = bbox [1]
        w = bbox[2]
        h = bbox[3]
        x2 = x1 + w
        y2 = y1 + h
 
        if(h < MIN_CHAR_HEIGHT):
            #print('Bbox too short')
            continue
            
        #if(h > (MAX_CHAR_HEIGHT_PCT * im_height)):
            #print('BBox too high')
            continue
            
        if(h > (MAX_CHAR_WIDTH_PCT * im_width)):
            #print('BBox too wide')
            continue
            
        ord_bboxs.append(bbox)
        ord_contour_idxs.append(idx)
        
        bw_im[:,:] = 255
        
        cv2.drawContours(bw_im, contours, idx, 0, -1, cv2.CV_AA, 
        hierarchy, 1)
        
        lett_im = cv2.copyMakeBorder(bw_im[y1:y2, x1:x2], 
        LETT_MARGIN, LETT_MARGIN, LETT_MARGIN, LETT_MARGIN, 
        cv2.BORDER_CONSTANT, value = 255)
        
        lett_im_w = w + (2 * LETT_MARGIN)
        lett_im_h = h + (2 * LETT_MARGIN)
        
        #lett_im = cv2.copyMakeBorder(lett_im, 0, 0,
        #lett_im_w, lett_im_w, cv2.BORDER_WRAP)
        
        #kernel = np.ones((KERNEL_SIZE,KERNEL_SIZE),np.uint8)
        #lett_im = cv2.dilate(lett_im, kernel)
        
        # Check if character is I
        
        #pt1 = (bbox[0], bbox[1])
        #pt2 = (pt1[0] + bbox[2], pt1[1] + bbox[3])
        
        #rgb_im_copy = rgb_im.copy()

        #cv2.rectangle(rgb_im_copy, pt1, pt2, (0,0,255)) 
        
        #cv2.imshow('lett_im', lett_im)
        
        bbox_area = w * h
        lett_im_area = lett_im_w * lett_im_h
        black_pels_nr = lett_im_area - cv2.countNonZero(lett_im)
        
        saturation = float(black_pels_nr) / float(bbox_area)
        #print('saturation', saturation)
        
        pt1 = (bbox[0], bbox[1])
        pt2 = (pt1[0] + bbox[2], pt1[1] + bbox[3])
        
        cv2.rectangle(rgb_im, pt1, pt2, (0,0,255))

        #cv2.imshow('rgb_im', rgb_im)
        #cv2.waitKey(0) 
        
        width_to_height_ratio = float(w) / float(h)
        
        #if((saturation > I_MIN_SATURATION) and
        #(width_to_height_ratio < I_MAX_WIDTH_TO_HEIGHT_RATIO)):
            #all_letters.append('i')
            #continue
        
        text = ''
        kernel_size = 0
        while((len(text) == 0) and (kernel_size <= KERNEL_MAX_SIZE )):
            
            # Dilate image
            if(kernel_size > 0):
                kernel = np.ones((kernel_size, kernel_size),np.uint8)
                lett_im = cv2.dilate(lett_im, kernel)
        
            kernel_size = kernel_size + 1
            shape_1 = lett_im.shape[1]
            shape_0 = lett_im.shape[0]
            depth = cv.IPL_DEPTH_8U
            bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
            cv.SetData(bitmap, lett_im.tostring(), 
                lett_im.dtype.itemsize * 1 * shape_1)
        
            tesseract.SetCvImage(bitmap,api)
            text = api.GetUTF8Text().rstrip()
            #print('text', text)   
            
        # Try to identify char by adding to image a known char
        if(len(text) == 0):
            lett_im = cv2.copyMakeBorder(bw_im[y1:y2, x1:x2], 
            LETT_MARGIN, LETT_MARGIN, LETT_MARGIN, 3 * LETT_MARGIN + h, 
            cv2.BORDER_CONSTANT, value = 255)
            text_size = h / PELS_TO_TEXT_SIZE_RATIO 
            cv2.putText(lett_im,'B', (w + LETT_MARGIN * 2,h), 
            cv2.FONT_HERSHEY_SIMPLEX, text_size, 0,2)
            
            #print('h', h)
            #cv2.imshow('lett_im 2', lett_im)
            #cv2.waitKey(0)
            
            # Transform image
            shape_1 = lett_im.shape[1]
            shape_0 = lett_im.shape[0]
            depth = cv.IPL_DEPTH_8U
            bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
            cv.SetData(bitmap, lett_im.tostring(), 
                lett_im.dtype.itemsize * 1 * shape_1)
        
            api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
            tesseract.SetCvImage(bitmap,api)
            text = api.GetUTF8Text().rstrip()
            #print('text 2', text)
            api.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)
            
            if(len(text) == 2):
                text = text[0]
           
        all_letters_str = all_letters_str + text
        all_letters.append(text)
            
        useful_contour_counter = useful_contour_counter + 1
        #print(all_letters_str)
        
    #cv2.imshow('rgb', rgb_im)
            
    #cv2.waitKey(0)
  
    # Divide letters by row
    rows = []
    rows_bboxs = []
    rows_contour_idxs = []
    # Index of letters that must not be considered anymore
    idx_black_list = []
    #print(all_letters)
    lett_idx = 0
    rgb_im_copy = rgb_im.copy() # TEST ONLY
    for lett in all_letters:
        if((lett_idx not in idx_black_list) and (len(lett) > 0)):
            
            idx_black_list.append(lett_idx)
            bbox = ord_bboxs[lett_idx]
            x1 = bbox[0]
            y1 = bbox [1]
            w = bbox[2]
            h = bbox[3]
            x2 = x1 + w
            y2 = y1 + h
            
            big_bbox = bbox
            
            row = lett
            row_bboxs = [bbox]
            
            contour_idx = ord_contour_idxs[lett_idx]
            row_contour_idxs = [contour_idx]
            
            #print('new idx')
            rgb_im_copy = rgb_im.copy()
            
            pt1 = (bbox[0], bbox[1])
            pt2 = (pt1[0] + bbox[2], pt1[1] + bbox[3])
        
            #cv2.rectangle(rgb_im_copy, pt1, pt2, (0,0,255)) # TEST ONLY
            
            for idx2 in range((lett_idx + 1),len(all_letters)):
                #print(idx2)
                if(idx2 not in idx_black_list):
                    #print('len(all_letters)', len(all_letters))
                    #print('len(ord_bboxs)', len(ord_bboxs))
                    #print('idx2', idx2)
                    
                    lett2 = all_letters[idx2]
                    bbox2 = ord_bboxs[idx2]
                    x12 = bbox2[0]
                    y12 = bbox2 [1]
                    w2 = bbox2[2]
                    h2 = bbox2[3]
                    x22 = x12 + w2
                    y22 = y12 + h2
                    
                    #pt1 = (bbox2[0], bbox2[1])
                    #pt2 = (pt1[0] + bbox2[2], pt1[1] + bbox2[3])
                    
                    #cv2.rectangle(rgb_im_copy, pt1, pt2, (0,0,255)) 
            
                    #cv2.imshow('rgb', rgb_im_copy)
                        
                    #cv2.waitKey(0)
                    
                    #print 'y1 = %d y2 = %d y12 = %d y22 = %d' % (y1, y2, y12, y22)
                    
                    #print 'step1'
                    
                    if(((y12 > (y1 - MAX_BBOX_DIFF)) and (y12 < y2)) 
                    or ((y22 > y1) and (y22 < (y2 + MAX_BBOX_DIFF)))):
                        lett2 = all_letters[idx2]
                        idx_black_list.append(idx2)
                        
                        # Discard letter if it is inside previous letter
                        big_x = big_bbox[0]
                        big_y = big_bbox[1]
                        big_w = big_bbox[2]
                        big_h = big_bbox[3]
                        big_x2 = big_x + big_w
                        big_y2 = big_y + big_h
                        
                        if(not((x12 > big_x) and (y12 > big_y) 
                        and (x22 < big_x2) and (y22 < big_y2))):
                        
                            row = row + lett2
                            
                            row_bboxs.append(bbox2)
                            
                            contour_idx = ord_contour_idxs[idx2]
                            
                            row_contour_idxs.append(contour_idx)
                            
                            big_bbox = bbox2
                        
                        #pt1 = (bbox2[0], bbox2[1])
                        #pt2 = (pt1[0] + bbox2[2], pt1[1] + bbox2[3])
                        
            rows.append(row)
            rows_bboxs.append(row_bboxs)
            rows_contour_idxs.append(row_contour_idxs)
            
        lett_idx = lett_idx + 1                     
     
    fm = face_models;
    if(face_models == None):
        fm = FaceModelsLBP();
        
    labels = fm.get_labels()
    
    print('rows', rows)
    
    row_idx = 0
    words = []
    for row in rows:
        
        bw_im[:,:] = 255
        
        for i in range(0, len(row)):
    
            lett = row[i]
            print('lett', lett)
            
            contour_idx = rows_contour_idxs[row_idx][i]
        
            cv2.drawContours(bw_im, contours, contour_idx, 
            0, -1, cv2.CV_AA, hierarchy, 1)
        
        # Transform image
        shape_1 = bw_im.shape[1]
        shape_0 = bw_im.shape[0]
        depth = cv.IPL_DEPTH_8U
        bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
        cv.SetData(bitmap, bw_im.tostring(), 
            bw_im.dtype.itemsize * 1 * shape_1)
    
        api.SetPageSegMode(tesseract.PSM_AUTO)
        tesseract.SetCvImage(bitmap,api)
        text = api.GetUTF8Text().rstrip()
        
        print('TEXT',text)
        if(len(text) > 0):
			row_words = text.split()
			for row_word in row_words:
				words.append(row_word)
        
        cv2.imshow('bw_im', bw_im)
        cv2.waitKey(0)
            
        row_idx = row_idx + 1
        
    print('words', words)
    rows = words
    
    if(labels != -1):
        assigned_label = ''
        eq_letters_nr = 0
        tot_letter_nr = 0
        lett_counter_list = []
        label_parts_len_list =  []
        lett_pct_list = []
        for label in labels:
            # Divide name(s) and surname(s)
            label_parts = label.split(LABEL_SEP)
            lett_counter = 0
            label_parts_len = 0
            
            for label_part in label_parts:
                label_parts_len = label_parts_len + len(label_part)
       
                # Consider each row separately
                row_lett_counter_l = []
                
                complete_check_found = False
                for row in rows:
                    
                    # Index of letters that must not be considered anymore
                    black_list = []
                    row_lett_counter = 0
                    start = 0 
                
                    for i in range(0, len(label_part)):
                        # For each letter in label part
                        lett = label_part[i]

                        lett_idx = row.lower().find(lett.lower(), start)
                        
                        #print(lett_idx)
                        if((lett_idx != -1) and (lett_idx not in black_list)):
                            row_lett_counter = row_lett_counter + 1
                            start = lett_idx + 1
                            black_list.append(lett_idx)

                        if(row_lett_counter == len(label_part)):
                            lett_counter = lett_counter + row_lett_counter
                            complete_check_found = True
                    row_lett_counter_l.append(row_lett_counter)
                    
                # Add to total best row check
                #print(row_lett_counter_l)
                if(not(complete_check_found)):
                    if(len(row_lett_counter_l) > 0):
                        lett_counter = lett_counter + max(row_lett_counter_l)
                
            if(lett_counter == label_parts_len):
                assigned_label = label
                eq_letters_nr = lett_counter
                tot_letter_nr = lett_counter
                break
            else:
                lett_counter_list.append(lett_counter)
                label_parts_len_list.append(label_parts_len)
                lett_pct = float(lett_counter) / label_parts_len
                lett_pct_list.append(lett_pct)
                
            print "Tag = %s (%d equal letters out of %d)" % (label, lett_counter, label_parts_len) # TEST ONLY
        
        if(len(assigned_label) == 0):
            label_idxs = [i[0] for i in sorted(enumerate(lett_pct_list), 
            key=lambda x:x[1], reverse = True)]
            assigned_label_idx = label_idxs[0]
            assigned_label = labels[assigned_label_idx]
            eq_letters_nr = lett_counter_list[assigned_label_idx]
            tot_letter_nr = label_parts_len_list[assigned_label_idx]
            
        print "Predicted tag = %s (%d equal letters out of %d)" % (assigned_label, eq_letters_nr, tot_letter_nr) # TEST ONLY
    
        cv2.imshow('rgb', rgb_im_copy)
            
        cv2.waitKey(0)

####    TEST ONLY      ####

use_all_images = True

if (use_all_images):
   
    folder = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video Videolina\Originali'
    
    fm = FaceModelsLBP()
    
    for image in listdir(folder):
        
        image_complete_path = folder + '\\' + image;
        
        get_tag_from_image(image_complete_path, fm)
        
else:
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Caption detection\Baldaccini.bmp'
    image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video Videolina\Originali\BaldacciniDOcchiChiusi.jpg'
    #image_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE - locale\OCR\OCR\Fotogrammi da video YouTube\Originali\Fisichella_Giancarlo.jpg'
    fm = FaceModelsLBP()
    
    get_tag_from_image(image_path, fm)
    
