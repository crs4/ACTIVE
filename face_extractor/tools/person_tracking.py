import cv2
import numpy as np
import os

import constants as c
from face_detection import detect_faces_in_image
from object_detection import background_subtraction_on_images
from utils import compare_clothes, save_YAML_file


def get_clothing_model_from_sequence(frame_seq, params):
    """
    Calculate clothing model from frame sequence

    :type frame_seq: list
    :param frame_seq: list of paths of frame sequence

    :type params: dictionary
    :param params: configuration parameters (see table)

    :rtype: list
    :returns: clothing model

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    clothes_bounding_box_height                   Height of bounding box for clothes
                                                  (in % of the face bounding box height)    1.0
    clothes_bounding_box_width                    Width of bounding box for clothes         2.0
                                                  (in % of the face bounding box width)
                                                  If True, use mask for HSV values in clothing recognition
    neck_height                                   Height of neck (in % of the               0.0
                                                  face bounding box height)
    nr_of_HSV_channels_in_clothing_recognition    Number of HSV channels used
                                                  in clothing recognition (1-3)             3
    use_LBP_in_clothing_recognition               If True, use LBP as features              False
                                                  for clothing recognition
    use_mask_in_clothing_recognition              If True, use mask for HSV values          True
                                                  in clothing recognition
    use_motion_mask_in_clothing_recognition       If True, calculate histograms only        False
                                                  on regions where motion is detected
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    face_detection_algorithm                      Classifier for face detection             'HaarCascadeFrontalFaceAlt2'
                                                  ('HaarCascadeFrontalFaceAlt',
                                                  'HaarCascadeFrontalFaceAltTree',
                                                  'HaarCascadeFrontalFaceAlt2',
                                                  'HaarCascadeFrontalFaceDefault',
                                                  'HaarCascadeProfileFace',
                                                  'HaarCascadeFrontalAndProfileFaces',
                                                  'HaarCascadeFrontalAndProfileFaces2',
                                                  'LBPCascadeFrontalface',
                                                  'LBPCascadeProfileFace' or
                                                  'LBPCascadeFrontalAndProfileFaces')
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch').
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    ============================================  ========================================  =============================
    """

    # Set parameters
    align_path = c.ALIGNED_FACES_PATH
    cl_pct_height = c.CLOTHES_BBOX_HEIGHT
    cl_pct_width = c.CLOTHES_BBOX_WIDTH
    hsv_channels = c.CLOTHING_REC_HSV_CHANNELS_NR
    neck_pct_height = c.NECK_HEIGHT
    use_LBP = c.CLOTHING_REC_USE_LBP
    use_mask = c.CLOTHING_REC_USE_MASK
    use_motion_mask = c.CLOTHING_REC_USE_MOTION_MASK
    if params:
        if c.ALIGNED_FACES_PATH_KEY in params:
            align_path = params[c.ALIGNED_FACES_PATH_KEY]
        if c.CLOTHES_BBOX_HEIGHT_KEY in params:
            cl_pct_height = params[c.CLOTHES_BBOX_HEIGHT_KEY]
        if c.CLOTHES_BBOX_WIDTH_KEY in params:
            cl_pct_width = params[c.CLOTHES_BBOX_WIDTH_KEY]
        if c.CLOTHING_REC_HSV_CHANNELS_NR_KEY in params:
            hsv_channels = params[c.CLOTHING_REC_HSV_CHANNELS_NR_KEY]
        if c.NECK_HEIGHT_KEY in params:
            neck_pct_height = params[c.NECK_HEIGHT_KEY]
        if c.CLOTHING_REC_USE_LBP_KEY in params:
            use_LBP = params[c.CLOTHING_REC_USE_LBP_KEY]
        if c.CLOTHING_REC_USE_MASK_KEY in params:
            use_mask = params[c.CLOTHING_REC_USE_MASK_KEY]
        if c.CLOTHING_REC_USE_MOTION_MASK_KEY in params:
            use_motion_mask = params[c.CLOTHING_REC_USE_MOTION_MASK_KEY]

    # No alignment must be carried out
    if params is None:
        params = {}
    params[c.USE_EYES_POSITION_KEY] = False

    image_masks = None
    if use_motion_mask:
        # Get regions with detected moving objects
        image_masks = background_subtraction_on_images(frame_seq)

    # Get clothing information from sequence
    model = []
    counter = 0
    for im_path in frame_seq:

        if use_motion_mask and (counter == 0):
            # Moving objects are detected since second frame
            counter += 1
            continue

        # Detect faces in image and take first result
        result_dict = detect_faces_in_image(im_path, align_path, params, False)
        if c.FACES_KEY in result_dict:
            faces = result_dict[c.FACES_KEY]
            if len(faces) > 0:
                face_dict = faces[0]
                face_bbox = face_dict[c.BBOX_KEY]
                face_x0 = face_bbox[0]
                face_y0 = face_bbox[1]
                face_width = face_bbox[2]
                face_height = face_bbox[3]
                face_x1 = face_x0 + face_width
                face_y1 = face_y0 + face_height

                # Get region of interest for clothes
                clothes_width = int(face_width * cl_pct_width)
                clothes_height = int(face_height * cl_pct_height)
                clothes_x0 = int(face_x0 + face_width / 2.0 - clothes_width / 2.0)

                clothes_y0 = int(
                    face_y0 + face_height + (face_height * neck_pct_height))
                clothes_x1 = clothes_x0 + clothes_width
                clothes_y1 = clothes_y0 + clothes_height

                im = cv2.imread(im_path)
                roi = im[clothes_y0:clothes_y1, clothes_x0:clothes_x1]

                # Check if bounding box is entirely contained by frame
                im_height, im_width, channels = im.shape
                if ((clothes_x0 < 0) or (clothes_x1 > im_width)
                        or (clothes_y0 < 0) or (clothes_y1 > im_height)):
                    print('Bounding box not entirely contained by frame')
                    return None

                if use_LBP:
                    # Use LBP histograms
                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    recognizer = cv2.createLBPHFaceRecognizer(1, 8, 1, 1)
                    recognizer.train(
                        np.asarray([np.asarray(roi_gray, dtype=np.uint8)]),
                        np.asarray([0]))

                    hist = recognizer.getMatVector("histograms")[0][0]
                    model.append([hist])

                else:
                    # Use HSV histograms
                    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    mask = None
                    if use_mask:
                        mask = cv2.inRange(roi_hsv,
                                           np.array((0., 60., 32.)),
                                           np.array((180., 255., 255.)))

                    if image_masks:
                        motion_mask = None
                        im_motion_mask = image_masks[counter]
                        roi_motion_mask = im_motion_mask[clothes_y0:clothes_y1, clothes_x0:clothes_x1]
                        if use_mask:
                            mask = roi_motion_mask & mask
                        else:
                            mask = roi_motion_mask

                    hists = []
                    for ch in range(0, hsv_channels):
                        hist = cv2.calcHist(
                            [roi_hsv], [ch], mask, [256], [0, 255])

                        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

                        hists.append(hist)

                    model.append(hists)

        counter += 1

    return model


def find_person_by_clothes(
        img_path, ref_img_path, face_bbox, params=None, show_results=False):
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
    :param params: dictionary with configuration parameters (see table)

    :type show_results: boolean
    :param show_results: show (True) or do not show (False)
                         image with detected faces

    :rtype: tuple or None
    :returns: if person is found, predicted face bounding box in image,
             given as tuple (x, y, width, height), otherwise None

    ============================================  ========================================  ==============
    Key                                           Value                                     Default value
    ============================================  ========================================  ==============
    person_tracking_clothes_bbox_height           Height of bounding box for clothes        1.0
                                                  (in % of the face bounding box height)
    person_tracking_clothes_bbox_width            Width of bounding box for clothes         2.0
                                                  (in % of the face bounding box width)
    person_tracking_neck_height                   Height of neck (in % of the               0.0
                                                  face bounding box height)
    nr_of_hsv_channels_in_person_tracking         Number of HSV channels used               2
                                                  in person tracking (1-2)
    use_mask_in_person_tracking                   If True, use a mask for HSV values        False
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    ============================================  ========================================  ==============
    """

    result = None

    ref_img = cv2.imread(ref_img_path, cv2.IMREAD_COLOR)

    face_x0 = face_bbox[0]
    face_y0 = face_bbox[1]
    face_width = face_bbox[2]
    face_height = face_bbox[3]
    face_x1 = face_x0 + face_width
    face_y1 = face_y0 + face_height

    # Set parameters
    cl_pct_height = c.PERSON_TRACKING_CLOTHES_BBOX_HEIGHT
    cl_pct_width = c.PERSON_TRACKING_CLOTHES_BBOX_WIDTH
    neck_pct_height = c.PERSON_TRACKING_NECK_HEIGHT
    dim = c.PERSON_TRACKING_HSV_CHANNELS_NR
    use_mask = c.PERSON_TRACKING_USE_MASK
    min_size_width = c.FACE_DETECTION_MIN_SIZE_WIDTH
    min_size_height = c.FACE_DETECTION_MIN_SIZE_HEIGHT

    if params is not None:
        if c.PERSON_TRACKING_CLOTHES_BBOX_HEIGHT_KEY in params:
            cl_pct_height = params[c.PERSON_TRACKING_CLOTHES_BBOX_HEIGHT_KEY]
        if c.PERSON_TRACKING_CLOTHES_BBOX_WIDTH_KEY in params:
            cl_pct_width = params[c.PERSON_TRACKING_CLOTHES_BBOX_WIDTH_KEY]
        if c.PERSON_TRACKING_NECK_HEIGHT_KEY in params:
            neck_pct_height = params[c.PERSON_TRACKING_NECK_HEIGHT_KEY]
        if c.PERSON_TRACKING_HSV_CHANNELS_NR_KEY in params:
            dim = params[c.PERSON_TRACKING_HSV_CHANNELS_NR_KEY]
        if c.PERSON_TRACKING_USE_MASK_KEY in params:
            use_mask = params[c.PERSON_TRACKING_USE_MASK_KEY]
        if c.MIN_SIZE_WIDTH_KEY in params:
            min_size_width = params[c.MIN_SIZE_WIDTH_KEY]
        if c.MIN_SIZE_HEIGHT_KEY in params:
            min_size_height = params[c.MIN_SIZE_HEIGHT_KEY]

    # Get region of interest for clothes
    clothes_width = int(face_width * cl_pct_width)
    clothes_height = int(face_height * cl_pct_height)
    clothes_x0 = int(face_x0 + face_width / 2.0 - clothes_width / 2.0)

    clothes_y0 = int(
        face_y0 + face_height + (face_height * neck_pct_height))
    clothes_x1 = clothes_x0 + clothes_width
    clothes_y1 = clothes_y0 + clothes_height

    # Check if bounding box is entirely contained by frame
    im_height, im_width, channels = ref_img.shape
    if ((clothes_x0 < 0) or (clothes_x1 > im_width)
            or (clothes_y0 < 0) or (clothes_y1 > im_height)):
        return result

    rgb_roi = ref_img[clothes_y0:clothes_y1, clothes_x0:clothes_x1]

    # Transform region of interest in HSV
    hsv_roi = cv2.cvtColor(rgb_roi, cv2.COLOR_BGR2HSV)

    # Apply mask

    if show_results:
        # Show bounding boxes for clothes and face in reference image
        cv2.rectangle(
            ref_img, (clothes_x0, clothes_y0), (clothes_x1, clothes_y1),
            (0, 0, 255), 3, 8, 0)
        cv2.rectangle(
            ref_img, (face_x0, face_y0), (face_x1, face_y1),
            (255, 0, 0), 3, 8, 0)
        cv2.imshow('Reference image', ref_img)
        cv2.waitKey(0)

    mask_roi = None
    mask_lower_boundaries = np.array((0., 60., 32.))
    mask_upper_boundaries = np.array((180., 255., 255.))
    if use_mask:
        mask_roi = cv2.inRange(
            hsv_roi, mask_lower_boundaries, mask_upper_boundaries)

    # Calculate histogram
    # hist = cv2.calcHist([hsv_roi], [0], mask_roi, [256], [0, 255])
    # cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    # hist = hist.reshape(-1)
    channels = range(0, dim)
    size_array = [256] * dim
    ranges_array = [0, 255] * dim
    hist = cv2.calcHist(
        [hsv_roi], channels, mask_roi, size_array, ranges_array)

    # Find region with similar colors in image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    prob = cv2.calcBackProject([hsv_img], channels, hist, ranges_array, 1)
    mask_img = None
    if use_mask:
        mask_img = cv2.inRange(
            hsv_img, mask_lower_boundaries, mask_upper_boundaries)
        prob &= mask_img
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    track_box, track_window = cv2.CamShift(
        prob, (clothes_x0, clothes_y0, clothes_width, clothes_height),
        term_crit)
    height, width, channels = img.shape

    clothes_x0 = track_window[0]
    clothes_y0 = track_window[1]
    clothes_width = track_window[2]
    clothes_height = track_window[3]
    clothes_x1 = clothes_x0 + clothes_width
    clothes_y1 = clothes_y0 + clothes_height

    # Check size of track window
    min_clothes_width = min_size_width * cl_pct_width
    min_clothes_height = min_size_height * cl_pct_height
    if ((clothes_width < min_clothes_width)
            or (clothes_height < min_clothes_height)):
        return result

    # Get predicted face bounding box
    face_width = int(clothes_width / cl_pct_width)
    face_height = int(clothes_height / cl_pct_height)
    face_x0 = int(clothes_x0 - face_width / 2.0 + clothes_width / 2.0)
    face_y0 = int(clothes_y0 - face_height - (face_height * neck_pct_height))
    face_x1 = face_x0 + face_width
    face_y1 = face_y0 + face_height

    im_height, im_width, channels = img.shape
    # Check if bounding box is entirely contained by frame
    if ((face_x0 >= 0) and (face_x1 <= im_width)
            and (face_y0 >= 0) and (face_y1 <= im_height)):
        result = (face_x0, face_y0, face_width, face_height)

    if show_results:
        # Show back-projection
        cv2.imshow('back projection', prob)
        cv2.waitKey(0)

    if show_results:
        # Show bounding boxes for clothes and face in image
        cv2.rectangle(
            img, (clothes_x0, clothes_y0), (clothes_x1, clothes_y1),
            (0, 0, 255), 3, 8, 0)
        cv2.rectangle(
            img, (face_x0, face_y0), (face_x1, face_y1),
            (255, 0, 0), 3, 8, 0)

        cv2.imshow('image', img)
        cv2.waitKey(0)

    return result


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

    im_name = os.path.basename(im_path)
    cv2.imshow(im_name, rgb_image)
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

def create_ann_file_for_dataset(dataset_path, ann_file_path, params=None):
    """
    Create YAML file with annotations for given dataset.
    For each image in the dataset,
    posizion and size of the found face is stored.

    :type dataset_path: string
    :param dataset_path: path of dataset

    :type ann_file_path: string
    :param ann_file_path: path of file that will contain annotations

    :type params: dictionary
    :param params: configuration parameters (see table)

    ============================================  ========================================  =============================
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  =============================
    aligned_faces_path                            Path of directory for aligned faces
    check_eye_positions                           If True, check eye positions              True
    classifiers_dir_path                          Path of directory with OpenCV
                                                  cascade classifiers
    eye_detection_classifier                      Classifier for eye detection              'haarcascade_mcs_lefteye.xml'
    face_detection_algorithm                      Classifier for face detection             'HaarCascadeFrontalFaceAlt2'
                                                  ('HaarCascadeFrontalFaceAlt',
                                                  'HaarCascadeFrontalFaceAltTree',
                                                  'HaarCascadeFrontalFaceAlt2',
                                                  'HaarCascadeFrontalFaceDefault',
                                                  'HaarCascadeProfileFace',
                                                  'HaarCascadeFrontalAndProfileFaces',
                                                  'HaarCascadeFrontalAndProfileFaces2',
                                                  'LBPCascadeFrontalface',
                                                  'LBPCascadeProfileFace' or
                                                  'LBPCascadeFrontalAndProfileFaces')
    flags                                         Flags used in face detection              'DoCannyPruning'
                                                  ('DoCannyPruning', 'ScaleImage',
                                                  'FindBiggestObject', 'DoRoughSearch').
                                                  If 'DoCannyPruning' is used, regions
                                                  that do not contain lines are discarded.
                                                  If 'ScaleImage' is used, image instead
                                                  of the detector is scaled
                                                  (it can be advantegeous in terms of
                                                  memory and cache use).
                                                  If 'FindBiggestObject' is used,
                                                  only the biggest object is returned
                                                  by the detector.
                                                  'DoRoughSearch', used together with
                                                  'FindBiggestObject',
                                                  terminates the search as soon as
                                                  the first candidate object is found
    min_neighbors                                 Mininum number of neighbor bounding       5
                                                  boxes for retaining face detection
    min_size_height                               Minimum height of face detection          20
                                                  bounding box (in pixels)
    min_size_width                                Minimum width of face detection           20
                                                  bounding box (in pixels)
    scale_factor                                  Scale factor between two scans            1.1
                                                  in face detection
    max_eye_angle                                 Maximum inclination of the line           0.125
                                                  connecting the eyes
                                                  (in % of pi radians)
    min_eye_distance                              Minimum distance between eyes             0.25
                                                  (in % of the width of the face
                                                  bounding box)
    nose_detection_classifier                     Classifier for nose detection             'haarcascade_mcs_nose.xml'
    software_test_file                            Path of image to be used for
                                                  software test
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    ============================================  ========================================  =============================
    """

    # Set parameters
    align_path = c.ALIGNED_FACES_PATH
    if params:
        if c.ALIGNED_FACES_PATH_KEY in params:
            align_path = params[c.ALIGNED_FACES_PATH_KEY]

    ann_dict = {}
    for subject_dir in os.listdir(dataset_path):
        subject_path = os.path.join(dataset_path, subject_dir)
        for im_name in os.listdir(subject_path):
            # Path of image relative to dataset path
            rel_im_path = os.path.join(subject_dir, im_name)
            ann_dict[rel_im_path] = {}
            print('rel_im_path', rel_im_path)

            # Full path of image
            im_path = os.path.join(subject_path, im_name)

            # Detect faces in image and take first result

            result_dict = detect_faces_in_image(
                im_path, align_path, params, False)

            if c.FACES_KEY in result_dict:
                faces = result_dict[c.FACES_KEY]
                if len(faces) > 0:
                    face_dict = faces[0]
                    bbox = face_dict[c.BBOX_KEY]
                    ann_dict[rel_im_path][c.BBOX_KEY] = bbox

    save_YAML_file(ann_file_path, ann_dict)