import cv2
import numpy as np
import tesseract

counter = 8

im_path = r'C:\Users\Maurizio\Documents\File di test\OCR\Orig' + str(counter) +'.jpg'

rgb_im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

#cv2.imshow('Original image', rgb_im)
#cv2.waitKey(0)

flags = cv2.THRESH_BINARY | cv2.THRESH_OTSU
th, bw_im = cv2.threshold(rgb_im, 128, 255, flags)

kernel_size = 3

# Erode image
if(kernel_size > 0):
    kernel = np.ones((kernel_size, kernel_size),np.uint8)
    bw_im = cv2.erode(bw_im, kernel)

#cv2.imshow('B/w image', bw_im)
#cv2.waitKey(0)

new_im_path = r'C:\Users\Maurizio\Documents\File di test\OCR\BW' + str(counter) +'.jpg'

cv2.imwrite(new_im_path, bw_im)

# Tesseract init
api = tesseract.TessBaseAPI()
api.Init(".","eng",tesseract.OEM_DEFAULT)
#api.SetVariable("tessedit_char_whitelist",
#"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
api.SetPageSegMode(tesseract.PSM_AUTO)

# Transform image
shape_1 = bw_im.shape[1]
shape_0 = bw_im.shape[0]
depth = cv2.cv.IPL_DEPTH_8U
bitmap = cv2.cv.CreateImageHeader((shape_1, shape_0), depth, 1)
cv2.cv.SetData(bitmap, bw_im.tostring(), 
    bw_im.dtype.itemsize * 1 * shape_1)

api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
tesseract.SetCvImage(bitmap,api)
text = api.GetUTF8Text()

text_path = r'C:\Users\Maurizio\Documents\File di test\OCR\Text' + str(counter) + '.txt'
with open(text_path, 'w') as out:
    out.write(text)
    
print(text)
