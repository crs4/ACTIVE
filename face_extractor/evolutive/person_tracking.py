import cv2
import numpy as np
import os
import sys

path_to_be_appended = ".."
sys.path.append(path_to_be_appended)

import tools.constants as c
from tools.face_detection import detect_faces_in_image


def find_person_by_clothes(img_path, ref_img_path, face_bbox, params=None):
    """
    Find person in image by using information about clothes

    :type: img_path: string
    :param img_path: path of image where person must be searched

    :type ref_img_path: string
    :param ref_img_path: path of reference image where person's face is visible

    :type face_bbox: tuple
    :param face_bbox: face bounding box in reference image,
    given as tuple (x, y, width, height)

    :type params: dictionary
    :param params: dictionary with configuration parameters

    :rtype: tuple or None
    :return: if person is found, predicted face bounding box in image,
    given as tuple (x, y, width, height), otherwise None
    """

    ref_img = cv2.imread(ref_img_path, cv2.IMREAD_COLOR)

    face_x = face_bbox[0]
    face_y = face_bbox[1]
    face_width = face_bbox[2]
    face_height = face_bbox[3]

    # Set parameters
    cl_pct_height = c.CLOTHES_BBOX_HEIGHT
    cl_pct_width = c.CLOTHES_BBOX_WIDTH
    neck_pct_height = c.NECK_HEIGHT

    if params is not None:
        if c.CLOTHES_BBOX_HEIGHT_KEY in params:
            cl_pct_height = params[c.CLOTHES_BBOX_HEIGHT_KEY]
        if c.CLOTHES_BBOX_WIDTH_KEY in params:
            cl_pct_width = params[c.CLOTHES_BBOX_WIDTH_KEY]
        if c.NECK_HEIGHT_KEY in params:
            neck_pct_height = params[c.NECK_HEIGHT_KEY]

    # Get region of interest for clothes
    clothes_width = int(face_width * cl_pct_width)
    clothes_height = int(face_height * cl_pct_height)
    clothes_x0 = int(face_x + face_width / 2.0 - clothes_width / 2.0)

    clothes_y0 = int(
        face_y + face_height + (face_height * neck_pct_height))
    clothes_x1 = clothes_x0 + clothes_width
    clothes_y1 = clothes_y0 + clothes_height

    rgb_roi = ref_img[clothes_y0:clothes_y1, clothes_x0:clothes_x1]

    # Transform region of interest in HSV
    hsv_roi = cv2.cvtColor(rgb_roi, cv2.COLOR_BGR2HSV)

    # Apply mask

    mask_roi = cv2.inRange(
        hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

    mask_roi = None
    # Calculate histogram
    # hist = cv2.calcHist([hsv_roi], [0], mask_roi, [256], [0, 255])
    # cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    # hist = hist.reshape(-1)
    dim = 2  # TODO INSERT IN NEW CONSTANTS
    channels = range(0, dim)
    size_array = [256] * dim
    ranges_array = [0, 255] * dim
    hist = cv2.calcHist(
        [hsv_roi], channels, mask_roi, size_array, ranges_array)


    # TODO DELETE TEST ONLY SHOW BBOX FOR CLOTHES IN REFERENCE IMAGE
    cv2.rectangle(ref_img, (clothes_x0, clothes_y0), (clothes_x1, clothes_y1),
                  (255, 0, 0), 3, 8, 0)
    cv2.imshow('Reference image', ref_img)
    cv2.waitKey(0)

    # Find region with similar colors in image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_img = cv2.inRange(
        hsv_img, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    # prob = cv2.calcBackProject([hsv_img], [0], hist, [0, 180], 1)
    prob = cv2.calcBackProject([hsv_img], channels, hist, ranges_array, 1)
    # prob &= mask_img
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    track_box, track_window = cv2.CamShift(
        prob, (clothes_x0, clothes_y0, clothes_width, clothes_height),
        term_crit)

    # TODO DELETE TEST ONLY SHOW BACKPROJECTION
    cv2.imshow('back projection', prob)
    cv2.waitKey(0)

    # TODO DELETE TEST ONLY SHOW BBOX FOR CLOTHES IN IMAGE
    track_x0 = track_window[0]
    track_y0 = track_window[1]
    track_w = track_window[2]
    track_h = track_window[3]

    cv2.rectangle(
        img, (track_x0, track_y0), (track_x0 + track_w, track_y0 + track_h),
        (0, 0, 255), 3, 8, 0)

    cv2.imshow('image', img)
    cv2.waitKey(0)


# # ref_img_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\80 persone\Sanna_Vittorio\Sanna_Vittorio -- 477.jpg'
# ref_img_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\80 persone\Mameli_Giacomo\Mameli_Giacomo -- 328.jpg'
# # img_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\80 persone\Sanna_Vittorio\Sanna_Vittorio -- 303.jpg'
# img_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-960I-80P-whole_images\80 persone\Mameli_Giacomo\Mameli_Giacomo -- 16.jpg'
# align_path = r'C:\Users\Maurizio\Documents\Risultati test\Person tracking\Aligned faces'
# det_result = detect_faces_in_image(ref_img_path, align_path, None, False)
# faces = det_result[c.FACES_KEY]
# face_dict = faces[0]
# face_bbox = face_dict[c.BBOX_KEY]
# find_person_by_clothes(img_path, ref_img_path, face_bbox)

def show_face_and_clothing_bboxes(im_path, params=None):
    """
    Show bounding boxes of faces found in given image
    and of the relative clothing

    :im_path: string
    :im_path: path of image

    :params: dictionary
    :params: dictionary with configuration parameters
    """

    # Set parameters
    align_path = c.ALIGNED_FACES_PATH
    clothing_width_pct = c.CLOTHES_BBOX_WIDTH
    clothing_height_pct = c.CLOTHES_BBOX_HEIGHT
    if params:
        if c.ALIGNED_FACES_PATH_KEY in params:
            align_path = params[c.ALIGNED_FACES_PATH_KEY]
        if c.CLOTHES_BBOX_WIDTH_KEY in params:
            clothing_width_pct = params[c.CLOTHES_BBOX_WIDTH_KEY]
        if c.CLOTHES_BBOX_HEIGHT_KEY in params:
            clothing_height_pct = params[c.CLOTHES_BBOX_HEIGHT_KEY]

    rgb_image = cv2.imread(im_path, cv2.IMREAD_COLOR)



    result_dict = detect_faces_in_image(im_path, align_path, params, False)

    faces = result_dict[c.FACES_KEY]

    for face_dict in faces:
        (x, y, w, h) = face_dict[c.BBOX_KEY]
        cv2.rectangle(rgb_image, (x, y), (x + w, y + h), (255, 0, 0), 4)
        cl_w = int(clothing_width_pct * w)
        cl_h = int(clothing_height_pct * h)
        cl_x = int(x + w / 2.0 - cl_w / 2.0)
        cl_y = int(y + h)
        cv2.rectangle(rgb_image, (cl_x, cl_y),
                      (cl_x + cl_w, cl_y + cl_h), (0, 0, 255), 4)

    cv2.imshow(im_path, rgb_image)
    cv2.waitKey(0)

def show_face_and_clothing_bboxes_in_dir(dir_path, params=None):
    """
    Show bounding boxes of faces found in images inside given directory
    and of the relative clothing

    :im_path: string
    :im_path: path of directory

    :params: dictionary
    :params: dictionary with configuration parameters
    """

    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            im_path = os.path.join(path, name)
            show_face_and_clothing_bboxes(im_path)

dir_path = r'C:\Users\Maurizio\Documents\Dataset\Evolutive\80 persone'
show_face_and_clothing_bboxes_in_dir(dir_path)
