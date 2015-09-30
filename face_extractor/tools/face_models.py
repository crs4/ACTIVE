import constants as c
import cv2
import cv2.cv as cv
import face_detection as fd
import utils
import numpy as np
import os
import shutil
import sys
import uuid


class FaceModels:
    """
    The face models used by the
    people recognition algorithms.

    :type params: dictionary
    :param params: configuration parameters (see table)

    :type models: list
    :param models: list with models for people recognition

    ============================================  ========================================  =============================
    Key                                           Value                                     Default value
    ============================================  ========================================  =============================
    aligned_faces_path                            Default path of directory
                                                  for aligned faces
    global_face_models_min_diff                   Minimum distance between faces            5
                                                  in global face models
    global_face_recognition_dir_path              Path of directory with people
                                                  recognition data
    global_face_recognition_threshold             Threshold for retaining prediction        8
                                                  in global face recognition
                                                  (faces whose prediction has a
                                                  confidence value greater than this
                                                  will be considered unknown)
    LBP_grid_x                                    Number of columns in grid                 4
                                                  used for calculating LBP
    LBP_grid_y                                    Number of columns in grid                 8
                                                  used for calculating LBP
    LBP_neighbors                                 Number of neighbors                       8
                                                  used for calculating LBP
    LBP_radius                                    Radius used                               1
                                                  for calculating LBP (in pixels)
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
    use_nose_pos_in_detection                     If True, detections with no good          False
                                                  nose position are discarded
    ============================================  ========================================  =============================
    """

    def __init__(self, params=None, models=None):
        """
        Initialize the face models

        :type params: dictionary
        :param params: configuration parameters

        :type models: list
        :param models: list with models for people recognition
        """

        self._params = params
        self._data_dir_path = c.GLOBAL_FACE_REC_DATA_DIR_PATH
        self._models = None
        self._en_models = None
        self._ext_models = models
        self._loaded_ext_models = None

        if params is not None:
            if c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY in params:
                self._data_dir_path = params[
                    c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY]

        # Create directory with people recognition data if it does not exist
        if not os.path.exists(self._data_dir_path):
            os.makedirs(self._data_dir_path)

    def add_face(self, label, tag, im_path, aligned_face=None, eye_pos=None,
                 bbox=None, enabled=True):
        """
        Add face to global training set for people recognition

        :type label: integer
        :param label: identifier of person in database

        :type tag: string
        :param tag: tag of person whom face belong to

        :type im_path: string
        :param im_path: path of image containing the face

        :type aligned_face: OpenCV image
        :param aligned_face: aligned face

        :type eye_pos: tuple
        :param eye_pos: a (left_eye_x, left_eye_y, right_eye_x, right_eye_y)
                        tuple containing eye positions


        :type bbox: tuple
        :param bbox: a (x, y, width, height) tuple containing position and size
                     of face bounding box in whole image

        :type enabled: boolean
        :param enabled: if True, face is also added
                        to models used for people recognition

        :rtype: boolean
        :returns: true if face has been added
        """

        ok = False

        try:

            # Set parameters
            radius = c.LBP_RADIUS
            neighbors = c.LBP_NEIGHBORS
            grid_x = c.LBP_GRID_X
            grid_y = c.LBP_GRID_Y

            if self._params is not None:
                if c.LBP_RADIUS_KEY in self._params:
                    radius = self._params[c.LBP_RADIUS_KEY]
                if c.LBP_NEIGHBORS_KEY in self._params:
                    neighbors = self._params[c.LBP_NEIGHBORS_KEY]
                if c.LBP_GRID_X_KEY in self._params:
                    grid_x = self._params[c.LBP_GRID_X_KEY]
                if c.LBP_GRID_Y_KEY in self._params:
                    grid_y = self._params[c.LBP_GRID_Y_KEY]

            # Check if face models are loaded
            if not self._models:
                self.load_models()

            # Create unique file name
            im_name = str(uuid.uuid4()) + '.png'

            # Convert label in string for use as directory name
            label_str = str(label)

            rel_im_path = os.path.join(label_str, im_name)

            training_set_path = os.path.join(
                self._data_dir_path, c.TRAINING_SET_DIR)

            whole_images_path = os.path.join(
                training_set_path, c.WHOLE_IMAGES_DIR)

            whole_images_subject_path = os.path.join(
                whole_images_path, label_str)

            whole_im_path = os.path.join(whole_images_path, rel_im_path)

            # Save aligned face
            aligned_faces_path = os.path.join(
                training_set_path, c.ALIGNED_FACES_DIR)

            aligned_faces_subject_path = os.path.join(
                aligned_faces_path, label_str)

            good_image = False

            if ((aligned_face is not None) and
                    (eye_pos is not None) and
                    (bbox is not None)):

                good_image = True

            else:

                # Detect face in whole image
                align_path = c.ALIGNED_FACES_PATH
                if (self._params and (
                        c.ALIGNED_FACES_PATH_KEY in self._params)):
                    align_path = self._params[c.ALIGNED_FACES_PATH_KEY]

                det_results = fd.detect_faces_in_image(
                    im_path, align_path, self._params, False)

                if det_results and (c.FACES_KEY in det_results):

                    faces = det_results[c.FACES_KEY]

                    if ((len(faces) == 1) and
                            (c.ALIGNED_FACE_FILE_NAME_KEY in faces[0]) and
                            (c.BBOX_KEY in faces[0]) and
                            (c.LEFT_EYE_POS_KEY in faces[0]) and
                            (c.RIGHT_EYE_POS_KEY in faces[0])):

                        file_name = faces[0][c.ALIGNED_FACE_FILE_NAME_KEY]
                        complete_file_name = (
                            file_name + c.ALIGNED_FACE_GRAY_SUFFIX + '.png')
                        aligned_file_path = os.path.join(
                            align_path, complete_file_name)

                        aligned_face = cv2.imread(
                            aligned_file_path, cv2.IMREAD_GRAYSCALE)

                        # Delete temporary files
                        complete_rgb_file_name = file_name + '.png'
                        rgb_file_path = os.path.join(
                            align_path, complete_rgb_file_name)
                        os.remove(rgb_file_path)
                        os.remove(aligned_file_path)

                        bbox = faces[0][c.BBOX_KEY]

                        eye_left = faces[0][c.LEFT_EYE_POS_KEY]

                        eye_right = faces[0][c.RIGHT_EYE_POS_KEY]

                        eye_pos = (
                            eye_left[0], eye_left[1], eye_right[0],
                            eye_right[1])

                        good_image = True

            if good_image:

                # Save whole image
                if not (os.path.exists(whole_images_subject_path)):
                    # Create directory
                    os.makedirs(whole_images_subject_path)

                whole_image = cv2.imread(im_path, cv2.IMREAD_COLOR)
                cv2.imwrite(whole_im_path, whole_image,
                            [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                if not (os.path.exists(aligned_faces_subject_path)):
                    # Create directory
                    os.makedirs(aligned_faces_subject_path)

                aligned_im_path = os.path.join(
                    aligned_faces_subject_path, im_name)

                cv2.imwrite(aligned_im_path, aligned_face,
                            [cv2.IMWRITE_PNG_COMPRESSION, 0])

                # Check if label is already in face models
                labels = self.get_labels()

                if label not in labels:

                    # Load file with tag-label associations
                    tag_label_associations_file = os.path.join(
                        self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
                    tag_label_associations = utils.load_YAML_file(
                        tag_label_associations_file)

                    if tag_label_associations:
                        # Add new tag with related label
                        tag_label_associations[label] = tag

                    else:
                        # Create dictionary with tag-label associations
                        tag_label_associations = {label: tag}

                    # Save new dictionary in YAML file
                    utils.save_YAML_file(
                        tag_label_associations_file, tag_label_associations)

                #  Save whole image with face bbox
                bbox_images_path = os.path.join(
                    training_set_path, c.BBOX_IMAGES_DIR)

                bbox_images_subject_path = os.path.join(
                    bbox_images_path, label_str)

                if not (os.path.exists(bbox_images_subject_path)):
                    # Create directory
                    os.makedirs(bbox_images_subject_path)

                bbox_im_path = os.path.join(bbox_images_path, rel_im_path)

                x0 = bbox[0]
                x1 = x0 + bbox[2]
                y0 = bbox[1]
                y1 = y0 + bbox[3]

                cv2.rectangle(whole_image, (x0, y0), (x1, y1), (0, 0, 255), 3,
                              8, 0)
                cv2.imwrite(bbox_im_path, whole_image,
                            [cv.CV_IMWRITE_PNG_COMPRESSION, 0])

                face_in_models = False

                new_lbl_array = [label]

                if self._models:

                    # Update models

                    min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF

                    if (self._params and
                            (c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY in self._params)):
                        min_diff = self._params[
                            c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY]

                    if min_diff > 0:
                        # Check if face is sufficiently different
                        # from other faces in models
                        (pred_label, conf) = self._models.predict(
                            np.asarray(aligned_face, dtype=np.uint8))

                        if conf >= min_diff:
                            self._models.update(
                                np.asarray(
                                    [np.asarray(aligned_face, dtype=np.uint8)]),
                                np.asarray(new_lbl_array))
                            face_in_models = True
                    else:
                        self._models.update(
                            np.asarray(
                                [np.asarray(aligned_face, dtype=np.uint8)]),
                            np.asarray(new_lbl_array))
                        face_in_models = True

                else:

                    # Create face recognizer
                    model = cv2.createLBPHFaceRecognizer(
                        radius,
                        neighbors,
                        grid_x,
                        grid_y)

                    # Create models
                    model.train(
                        np.asarray([np.asarray(aligned_face, dtype=np.uint8)]),
                        np.asarray(new_lbl_array))

                    face_in_models = True

                    self._models = model

                if face_in_models:
                    # Save file with face models
                    db_file_name = os.path.join(
                        self._data_dir_path, c.FACE_MODELS_FILE)

                    self._models.save(db_file_name)

                    # Check if face models used for people recognition
                    # are loaded
                    if not self._en_models:
                        self.load_enabled_models()
                    # Add face to models used for people recognition
                    if self._en_models:
                        self._en_models.update(
                            np.asarray(
                                [np.asarray(aligned_face, dtype=np.uint8)]),
                            np.asarray(new_lbl_array))
                    else:
                        # Create face recognizer
                        en_model = cv2.createLBPHFaceRecognizer(
                            radius,
                            neighbors,
                            grid_x,
                            grid_y)

                        # Create models
                        en_model.train(
                            np.asarray([np.asarray(aligned_face, dtype=np.uint8)]),
                            np.asarray(new_lbl_array))
                        self._en_models = en_model

                    # Save file with face models used for people recognition
                    en_db_file_name = os.path.join(
                        self._data_dir_path, c.ENABLED_FACE_MODELS_FILE)
                    self._en_models.save(en_db_file_name)

                else:
                    enabled = False

                # Load file with faces
                faces_file = os.path.join(
                    self._data_dir_path, c.FACES_FILE)
                faces_dict = utils.load_YAML_file(faces_file)
                if faces_dict is None:
                    # Create dictionary with association between
                    # image and related bbox and eye positions
                    faces_dict = {rel_im_path: {}}

                # Save face bbox and eye positions

                faces_dict[rel_im_path] = {}

                faces_dict[rel_im_path][c.BBOX_KEY] = bbox

                eye_left = (eye_pos[0], eye_pos[1])

                eye_right = (eye_pos[2], eye_pos[3])

                faces_dict[rel_im_path][c.LEFT_EYE_POS_KEY] = eye_left

                faces_dict[rel_im_path][c.RIGHT_EYE_POS_KEY] = eye_right

                faces_dict[rel_im_path][c.FACE_IN_MODELS_KEY] = face_in_models

                faces_dict[rel_im_path][c.ENABLED_KEY] = enabled

                # Save new dictionary in YAML file
                utils.save_YAML_file(faces_file, faces_dict)

                ok = True

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]

            raise

        return ok

    def add_blacklist_item(self, item):
        """
        Add given item to list of words that make
        the results of the caption recognition on a frame rejected

        :type item: string
        :param item: item to be added to blacklist

        :rtype: boolean
        :returns: true if item has been added to blacklist
        """

        blacklist_file_path = os.path.join(
            self._data_dir_path, c.WORD_BLACKLIST_FILE)

        blacklist = self.get_blacklist()

        if item not in blacklist:
            blacklist.append(item)

        utils.save_YAML_file(blacklist_file_path, blacklist)

    def change_label_to_face(self, im_name, old_label, new_label):
        """
        Change label to given face
        :type im_name: string
        :param im_name: name of image file

        :type old_label: int
        :param old_label: old label

        :type new_label: int
        :param new_label: new label
        """
        try:

            training_set_path = os.path.join(
                self._data_dir_path, c.TRAINING_SET_DIR)

            aligned_faces_path = os.path.join(
                training_set_path, c.ALIGNED_FACES_DIR)

            aligned_faces_old_label_path = os.path.join(
                aligned_faces_path, str(old_label))

            aligned_faces_new_label_path = os.path.join(
                aligned_faces_path, str(new_label))

            aligned_im_old_path = os.path.join(
                aligned_faces_old_label_path, im_name)

            # Load file with faces
            faces_file = os.path.join(
                self._data_dir_path, c.FACES_FILE)
            faces_dict = utils.load_YAML_file(faces_file)
            if faces_dict is None:
                print('No file with faces found')
                return

            if (os.path.exists(aligned_im_old_path) and
                    os.path.exists(aligned_faces_new_label_path)):

                # Move aligned face
                aligned_im_new_path = os.path.join(
                    aligned_faces_new_label_path, im_name)
                os.rename(aligned_im_old_path, aligned_im_new_path)

                # Move whole image
                whole_images_path = os.path.join(
                    training_set_path, c.WHOLE_IMAGES_DIR)
                whole_images_old_label_path = os.path.join(
                    whole_images_path, str(old_label))
                whole_images_new_label_path = os.path.join(
                    whole_images_path, str(new_label))
                whole_im_old_path = os.path.join(
                    whole_images_old_label_path, im_name)
                whole_im_new_path = os.path.join(
                    whole_images_new_label_path, im_name)
                os.rename(whole_im_old_path, whole_im_new_path)

                # Images with face bounding boxes
                bbox_images_path = os.path.join(
                    training_set_path, c.BBOX_IMAGES_DIR)
                bbox_images_old_label_path = os.path.join(
                    bbox_images_path, str(old_label))
                bbox_images_new_label_path = os.path.join(
                    bbox_images_path, str(new_label))
                bbox_im_old_path = os.path.join(
                    bbox_images_old_label_path, im_name)
                bbox_im_new_path = os.path.join(
                    bbox_images_new_label_path, im_name)
                os.rename(bbox_im_old_path, bbox_im_new_path)

                # Change key in dictionary with faces
                old_rel_im_path = os.path.join(str(old_label), im_name)
                new_rel_im_path = os.path.join(str(new_label), im_name)

                if old_rel_im_path in faces_dict:
                    faces_dict[new_rel_im_path] = (
                        faces_dict.pop(old_rel_im_path))

                # Save file with faces
                utils.save_YAML_file(faces_file, faces_dict)

                self.create_models_from_aligned_faces()

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]

            raise


    def change_tag_to_label(self, label, tag):
        """
        Change tag to given label

        :type label: integer
        :param label: label whose tag is to be changed

        :type tag: string
        :param tag: tag to be used for given label
        """

        # Load file with tag-label associations
        tag_label_associations_file = os.path.join(
            self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        tag_label_associations = utils.load_YAML_file(
            tag_label_associations_file)

        if label in tag_label_associations:
            tag_label_associations[label] = tag

        # Save file
        utils.save_YAML_file(
            tag_label_associations_file, tag_label_associations)


    def cluster_models(self):
        """
        Cluster face models
        """

        conf_threshold = c.GLOBAL_FACE_REC_THRESHOLD

        if self._params and c.GLOBAL_FACE_REC_THRESHOLD_KEY in self._params:
            conf_threshold = self._params[c.GLOBAL_FACE_REC_THRESHOLD_KEY]

        # Load models
        self.load_models()

        # Get histograms from models
        hists = self._models.getMatVector("histograms")

        # Get labels from models
        labels = self._models.getMat("labels")

        # Store indexes for each label

        label_dict = {}
        for i in range(0, len(hists)):
            label = labels[i][0]
            if label in label_dict:
                label_dict[label].append(i)
            else:
                label_dict[label] = [i]

        labels = label_dict.keys()

        clusters = []
        checked_labels = []
        for l1 in labels:
            if l1 not in checked_labels:
                # Do not consider this label anymore
                checked_labels.append(l1)
                l1_list = [int(l1)]  # List of labels with similar faces
                # Compare histograms for this label
                # to histograms for other labels
                for l2 in labels:
                    if l2 not in checked_labels:
                        # Get all histograms for this label
                        sim = False
                        for i1 in label_dict[l1]:
                            hist1 = hists[i1][0]
                            for i2 in label_dict[l2]:
                                hist2 = hists[i2][0]
                                diff = cv2.compareHist(
                                    hist1, hist2, cv.CV_COMP_CHISQR)
                                if diff < conf_threshold:
                                    l1_list.append(int(l2))
                                    checked_labels.append(l2)
                                    sim = True
                                    break
                            if sim:
                                break
                clusters.append(l1_list)

        # Save found clusters in file
        cluster_file = os.path.join(self._data_dir_path, c.CLUSTER_FILE)
        utils.save_YAML_file(cluster_file, clusters)


    def create_model_from_image_list(self, image_list, model_id):
        """
        Read images in given list and create face model

        :type image_list: list
        :param image_list: list of image paths

        :type model_id: integer
        :param model_id: model identifier

        :rtype: string
        :returns: path of created face model
        """

        # Set parameters
        radius = c.LBP_RADIUS
        neighbors = c.LBP_NEIGHBORS
        grid_x = c.LBP_GRID_X
        grid_y = c.LBP_GRID_Y
        min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF
        if self._params is not None:
            if c.LBP_RADIUS_KEY in self._params:
                radius = self._params[c.LBP_RADIUS_KEY]
            if c.LBP_NEIGHBORS_KEY in self._params:
                neighbors = self._params[c.LBP_NEIGHBORS_KEY]
            if c.LBP_GRID_X_KEY in self._params:
                grid_x = self._params[c.LBP_GRID_X_KEY]
            if c.LBP_GRID_Y_KEY in self._params:
                grid_y = self._params[c.LBP_GRID_Y_KEY]
            if c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY in self._params:
                min_diff = self._params[c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY]

        # Directory where face models are saved
        face_models_path = os.path.join(
            self._data_dir_path, c.FACE_MODELS_DIR)
        if not (os.path.exists(face_models_path)):
            # Create directory
            os.makedirs(face_models_path)

        # Create face recognizer
        model = cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)

        im_counter = 0
        for image_path in image_list:
            face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if im_counter == 0:
                # Create model
                model.train(
                    np.asarray([np.asarray(face, dtype=np.uint8)]),
                    np.asarray(model_id))
            else:
                # Update model
                if min_diff >= 0:
                    # Check if face is sufficiently different
                    # from other faces in models
                    (pred_label, conf) = model.predict(
                        np.asarray(face, dtype=np.uint8))

                    if conf >= min_diff:
                        model.update(
                            np.asarray([np.asarray(face, dtype=np.uint8)]),
                            np.asarray(model_id))
                else:
                    model.update(
                        np.asarray([np.asarray(face, dtype=np.uint8)]),
                        np.asarray(model_id))
            im_counter += 1

        # Save file with face models
        model_file_path = os.path.join(
            self._data_dir_path, c.FACE_MODELS_DIR, str(model_id))

        model.save(model_file_path)

        return model_file_path


    def create_models_from_aligned_faces(self, label_list=None, tag_list=None):
        """
        Read images in directory with aligned faces and create face models.
        Directory with aligned faces must contain
        one sub directory for each person.

        :type label_list: list
        :param label_list: list of labels for people.
                           If not provided, actual labels will not be changed

        :type tag_list: list
        :param tag_list: list of tags for people.
                         If not provided, actual tags will not be changed
        """

        try:

            model = None
            en_model = None

            training_set_path = os.path.join(
                self._data_dir_path, c.TRAINING_SET_DIR)

            aligned_faces_path = os.path.join(
                training_set_path, c.ALIGNED_FACES_DIR)

            subject_counter = 0

            use_given_labels = False
            if label_list is not None:

                # Check number and uniqueness of given labels
                for sub_dir_name in os.listdir(aligned_faces_path):
                    subject_counter += 1
                if ((len(label_list) == subject_counter) and
                        (len(label_list) == len(set(label_list)))):
                    use_given_labels = True
                else:
                    print('List of labels not good. '
                          'Actual labels will not be changed')

            use_given_tags = False
            if tag_list is not None:

                # Check number and uniqueness of given tags
                if ((len(tag_list) == subject_counter) and
                        (len(tag_list) == len(set(tag_list)))):
                    use_given_tags = True
                else:
                    print('List of tags not good. '
                          'Actual tags will not be changed')

            # Create face recognizer
            radius = c.LBP_RADIUS
            neighbors = c.LBP_NEIGHBORS
            grid_x = c.LBP_GRID_X
            grid_y = c.LBP_GRID_Y
            min_diff = c.GLOBAL_FACE_MODELS_MIN_DIFF

            if self._params is not None:
                if c.LBP_RADIUS_KEY in self._params:
                    radius = self._params[c.LBP_RADIUS_KEY]
                if c.LBP_NEIGHBORS_KEY in self._params:
                    neighbors = self._params[c.LBP_NEIGHBORS_KEY]
                if c.LBP_GRID_X_KEY in self._params:
                    grid_x = self._params[c.LBP_GRID_X_KEY]
                if c.LBP_GRID_Y_KEY in self._params:
                    grid_y = self._params[c.LBP_GRID_Y_KEY]
                if c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY in self._params:
                    min_diff = self._params[c.GLOBAL_FACE_MODELS_MIN_DIFF_KEY]

            # Load file with faces
            faces_file = os.path.join(
                self._data_dir_path, c.FACES_FILE)
            faces_dict = utils.load_YAML_file(faces_file)
            if faces_dict is None:
                print('No file with faces found')
                return

            # Load file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file)

            if tag_label_associations is None:
                print('No file with tag-label associations found')
                return

            im_counter = 0
            en_im_counter = 0
            subject_counter = 0

            old_sub_dir_name_list = []
            for sub_dir_name in os.listdir(aligned_faces_path):

                old_sub_dir_name_list.append(sub_dir_name)
                old_label = int(sub_dir_name)
                label = old_label

                # Check if old_label exists
                if old_label in tag_label_associations:

                    # Choose label for person
                    if use_given_labels:
                        label = label_list[subject_counter]

                        # Check if new_label does not exist
                        if label not in tag_label_associations:

                            # Change label in file with tag-label associations
                            tag_label_associations[label] = (
                                tag_label_associations.pop(old_label))

                        else:
                            print 'Label %s already exists' % label
                            return
                else:
                    print 'Label %s does not exist' % old_label
                    return

                if use_given_tags:
                    # Change tag for person
                    tag = tag_list[subject_counter]
                    tag_label_associations[label] = tag

                subject_path = os.path.join(
                    aligned_faces_path, sub_dir_name)

                for im_name in os.listdir(subject_path):

                    # print('im_name', im_name)

                    old_rel_im_path = os.path.join(sub_dir_name, im_name)
                    rel_im_path = old_rel_im_path
                    if use_given_labels:
                        # Change key in dictionary with faces
                        rel_im_path = os.path.join(str(label), im_name)

                        if old_rel_im_path in faces_dict:
                            faces_dict[rel_im_path] = (
                                faces_dict.pop(old_rel_im_path))
                        else:
                            print(
                                'Label %s does not exist' % old_rel_im_path)
                            return

                    im_path = os.path.join(subject_path, im_name)

                    face_in_models = False

                    face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

                    # If this is the first image train model,
                    # otherwise update it

                    if im_counter == 0:

                        model = cv2.createLBPHFaceRecognizer(
                            radius,
                            neighbors,
                            grid_x,
                            grid_y)

                        model.train(
                            np.asarray([np.asarray(face, dtype=np.uint8)]),
                            np.asarray(label))

                        face_in_models = True

                    else:

                        if min_diff > 0:
                            # Check if face is sufficiently different
                            # from other faces in models
                            (label, conf) = model.predict(
                                np.asarray(face, dtype=np.uint8))

                            if conf >= min_diff:
                                model.update(
                                    np.asarray(
                                        [np.asarray(face, dtype=np.uint8)]),
                                    np.asarray(label))

                                face_in_models = True

                        else:

                            model.update(
                                np.asarray([np.asarray(face, dtype=np.uint8)]),
                                np.asarray(label))

                            face_in_models = True

                    faces_dict[rel_im_path][
                        c.FACE_IN_MODELS_KEY] = face_in_models

                    # Update face model used for people recognition
                    enabled = False
                    if rel_im_path in faces_dict:
                        enabled = faces_dict[rel_im_path][c.ENABLED_KEY]

                    if enabled:
                        if en_im_counter == 0:

                            # Model with enabled faces
                            en_model = cv2.createLBPHFaceRecognizer(
                                radius,
                                neighbors,
                                grid_x,
                                grid_y)

                            en_model.train(
                                np.asarray([np.asarray(face, dtype=np.uint8)]),
                                np.asarray(label))
                        else:
                            en_model.update(
                                np.asarray([np.asarray(face, dtype=np.uint8)]),
                                np.asarray(label))
                        en_im_counter += 1

                    im_counter += 1

                subject_counter += 1

            if use_given_labels:
                # Change names of sub directories
                whole_images_path = os.path.join(
                    training_set_path, c.WHOLE_IMAGES_DIR)

                subject_counter = 0
                for old_sub_dir_name in old_sub_dir_name_list:
                    label = label_list[subject_counter]

                    # If name of sub directory does not equal label, change it
                    if not(old_sub_dir_name == str(label)):

                        # Aligned faces
                        old_subject_path = os.path.join(
                            aligned_faces_path, old_sub_dir_name)
                        new_subject_path = os.path.join(
                            aligned_faces_path, str(label))
                        os.rename(old_subject_path, new_subject_path)

                        # Whole images
                        old_subject_path = os.path.join(
                            whole_images_path, old_sub_dir_name)
                        new_subject_path = os.path.join(
                            whole_images_path, str(label))
                        os.rename(old_subject_path, new_subject_path)

                        # Images with face bounding boxes
                        bbox_images_path = os.path.join(
                            training_set_path, c.BBOX_IMAGES_DIR)
                        old_subject_path = os.path.join(
                            bbox_images_path, old_sub_dir_name)
                        new_subject_path = os.path.join(
                            bbox_images_path, str(label))
                        os.rename(old_subject_path, new_subject_path)

                    subject_counter += 1

            # Save file with all face models
            db_file_name = os.path.join(
                self._data_dir_path, c.FACE_MODELS_FILE)
            if model:
                model.save(db_file_name)
            else:
                # Remove file
                if os.path.exists(db_file_name):
                    os.remove(db_file_name)

            self._models = model

            # Save file with enabled face models
            en_db_file_name = os.path.join(
                self._data_dir_path, c.ENABLED_FACE_MODELS_FILE)
            if en_model:
                model.save(en_db_file_name)
            else:
                # Remove file
                if os.path.exists(en_db_file_name):
                    os.remove(en_db_file_name)

            self._en_models = en_model

            # Save file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            utils.save_YAML_file(
                tag_label_associations_file, tag_label_associations)
            # Save new dictionary in YAML file
            utils.save_YAML_file(faces_file, faces_dict)

        except IOError, (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except OSError, (errno, strerror):
            print "OS error({0}): {1}".format(errno, strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def create_models_from_whole_images(self, images_dir_path, label_list=None,
                                        tag_list=None, enabled=True):
        """
        Read images in given directory with images,
        detect and align faces in them and create face models.
        Directory with whole images must contain
        one sub directory for each person.

        :type images_dir_path: string
        :param images_dir_path: path of directory with images of people

        :type label_list: list
        :param label_list: list of labels for people.
                           If not provided, a progressive counter will be used

        :type tag_list: list
        :param tag_list: list of tags for people.
                         If not provided, names of sub directories will be used

        :type enabled: boolean
        :param enabled: if True, face are also added
                        to models used for people recognition

        :rtype: integer
        :returns: number of faces added to models
        """

        # Remove existing directories and files

        added_faces = 0
        subject_counter = 0

        use_given_labels = False
        if label_list is not None:

            # Check number and uniqueness of given labels
            for sub_dir_name in os.listdir(images_dir_path):
                subject_counter += 1
            if ((len(label_list) == subject_counter) and
                    (len(label_list) == len(set(label_list)))):
                use_given_labels = True
            else:
                print('List of labels not good. Models will not be created')
                return added_faces

        use_given_tags = False
        if tag_list is not None:

            # Check number and uniqueness of given tags
            if ((len(tag_list) == subject_counter) and
                    (len(tag_list) == len(set(tag_list)))):
                use_given_tags = True
            else:
                print('List of tags not good. Models will not be created')
                return added_faces

        try:

            # Remove existing data
            self.delete_models()

            # Iterate through sub directories with images of people
            subject_counter = 0  # Counter for sub directories

            for sub_dir_name in os.listdir(images_dir_path):

                # Choose label for person
                if use_given_labels:
                    label = label_list[subject_counter]
                else:
                    label = subject_counter

                # Choose tag for person
                if use_given_tags:
                    tag = tag_list[subject_counter]
                else:
                    tag = sub_dir_name

                subject_path = os.path.join(images_dir_path, sub_dir_name)

                for im_name in os.listdir(subject_path):

                    im_path = os.path.join(subject_path, im_name)

                    # Add image to face models
                    ok = self.add_face(label, tag, im_path, enabled=enabled)

                    if ok:
                        added_faces += 1

                subject_counter += 1

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]
            raise

        return added_faces


    def delete_model(self, model_id):
        """
        Delete model with given id

        :type model_id: integer
        :param model_id: identifier of model to be deleted

        :rtype: boolean
        :returns: True if model was successfully deleted
        """

        ok = False

        model_file_path = os.path.join(
            self._data_dir_path, c.FACE_MODELS_DIR, str(model_id))

        try:

            os.remove(model_file_path)

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]
            raise

        return ok




    def delete_models(self):
        """
        Delete all data for global face recognition
        """

        for item in os.listdir(self._data_dir_path):
            item_path = os.path.join(self._data_dir_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise


    def disable_faces(self, rel_im_tuples):
        """
        Do not use given faces for people recognition

        :type rel_im_tuples: list
        :param rel_im_tuples: a list of (label, im_name) tuples,
                              indicating labels and names of image
                              files that must be enabled
        """

        try:
            # Load file with faces
            faces_file = os.path.join(self._data_dir_path, c.FACES_FILE)
            faces_dict = utils.load_YAML_file(faces_file)

            if faces_dict:

                for rel_im_tuple in rel_im_tuples:
                    label = rel_im_tuple[0]
                    im_name = rel_im_tuple[1]
                    rel_im_path = os.path.join(str(label), im_name)
                    print('rel_im_path', rel_im_path)
                    if rel_im_path in faces_dict:
                        faces_dict[rel_im_path][c.ENABLED_KEY] = False

                # Save file with faces
                utils.save_YAML_file(faces_file, faces_dict)

                # Rebuild models
                self.create_models_from_aligned_faces()

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]

            raise


    def enable_faces(self, rel_im_tuples):
        """
        Use given faces for people recognition

        :type rel_im_tuples: list
        :param rel_im_tuples: a list of (label, im_name) tuples,
                              indicating labels and names of image files
                              that must be disabled
        """

        try:
            # Load file with faces
            faces_file = os.path.join(self._data_dir_path, c.FACES_FILE)
            faces_dict = utils.load_YAML_file(faces_file)

            if faces_dict:

                for rel_im_tuple in rel_im_tuples:
                    label = rel_im_tuple[0]
                    im_name = rel_im_tuple[1]
                    rel_im_path = os.path.join(str(label), im_name)
                    print('rel_im_path', rel_im_path)
                    if rel_im_path in faces_dict:
                        faces_dict[rel_im_path][c.ENABLED_KEY] = True

                # Save file with faces
                utils.save_YAML_file(faces_file, faces_dict)

                # Rebuild models
                self.create_models_from_aligned_faces()

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]

            raise


    def get_blacklist(self):
        """
        Get list of items that make the results
        of the caption recognition on a frame rejected

        :rtype: list
        :returns: a list containing all blacklist items
        """

        blacklist_file_path = os.path.join(
            self._data_dir_path, c.WORD_BLACKLIST_FILE)

        blacklist = []
        if os.path.exists(blacklist_file_path):
            blacklist = utils.load_YAML_file(blacklist_file_path)

        return blacklist

    def get_clusters(self):
        """
        Get clusters of models

        :rtype: list
        :return: list of lists with labels in each cluster
        """
        # Load found clusters from file
        cluster_file = os.path.join(self._data_dir_path, c.CLUSTER_FILE)
        clusters = utils.load_YAML_file(cluster_file)

        return clusters

    def get_labels(self):
        """
        Get all labels

        :rtype: set
        :returns: a set containing all labels
        """

        labels = []

        if self._ext_models:
            # Get model ids from model dictionaries
            for model_dict in self._ext_models:
                model_id = model_dict[c.MODEL_ID_KEY]
                labels.append(model_id)

        else:
            # Load file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file)

            if tag_label_associations:
                labels = tag_label_associations.keys()

        return set(labels)

    def get_labels_for_tag(self, tag):
        """
        Get labels corresponding to given tag

        :type tag: string
        :param tag: tag for which corresponding label is wanted

        :rtype: list
        :returns: list of labels corresponding to given tag
        """

        labels = []

        if self._ext_models:
            # Get model ids from model dictionaries
            for model_dict in self._ext_models:
                model_tag = model_dict[c.TAG_KEY]
                if model_tag == tag:
                    model_id = model_dict[c.MODEL_ID_KEY]
                    labels.append(model_id)
        else:
            # Load file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file)

            if tag_label_associations:
                for dict_label, dict_tag in tag_label_associations.items():
                    if dict_tag == tag:
                        labels.append(dict_label)

        return labels

    def get_tag(self, label):
        """
        Get tag corresponding to given label

        :type label: integer
        :param label: label for which corresponding tag is wanted

        :rtype: string
        :returns: tag corresponding to given label
        """

        tag = c.UNDEFINED_TAG

        if self._ext_models:
            # Get model ids from model dictionaries
            for model_dict in self._ext_models:
                model_id = model_dict[c.MODEL_ID_KEY]
                if model_id == label:
                    model_tag = model_dict[c.TAG_KEY]
                    return model_tag
        else:

            # Load file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file)

            if (tag_label_associations and
                    (label in tag_label_associations)):
                tag = tag_label_associations[label]

        return tag

    def get_tags(self):
        """
        Get all tags

        :rtype: set
        :returns: a set containing all tags
        """

        tags = []

        if self._ext_models:
            # Get model ids from model dictionaries
            for model_dict in self._ext_models:
                tag = model_dict[c.TAG_KEY]
                tags.append(tag)
        else:
            # Load file with tag-label associations
            tag_label_associations_file = os.path.join(
                self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
            tag_label_associations = utils.load_YAML_file(
                tag_label_associations_file, )

            if tag_label_associations:
                tags = tag_label_associations.values()

        return set(tags)


    def get_images_for_label(self, label):
        """
        Get image names for given label

        :rtype: list
        :return: list of image names
        """

        training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)

        aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)

        aligned_faces_subject_path = os.path.join(
            aligned_faces_path, str(label))

        images = []
        for im_name in os.listdir(aligned_faces_subject_path):
            images.append(im_name)

        return images


    def get_images_nr_for_label(self, label):
        """
        Get number of images for given label

        :type label: integer
        :param label: label for whom number of images is queried

        :rtype: integer
        :returns: number of images for given label
        """

        training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)

        aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)

        aligned_faces_subject_path = os.path.join(
            aligned_faces_path, str(label))

        images_nr = 0

        for image in os.listdir(aligned_faces_subject_path):
            images_nr += 1

        return images_nr

    def get_people_nr(self):
        """
        Get number of people in face model

        :rtype: integer
        :returns: number of people in face model
        """

        labels = self.get_labels()

        people_nr = len(labels)

        return people_nr

    def load_enabled_models(self):
        """
        Load face models used for people recognition

        :rtype: boolean
        :returns: True if models were successfully loaded,
                  False otherwise
        """

        ok = False

        db_file_path = os.path.join(
            self._data_dir_path, c.ENABLED_FACE_MODELS_FILE)

        # Load face recognizer

        if os.path.exists(db_file_path):
            self._en_models = cv2.createLBPHFaceRecognizer()

            self._en_models.load(db_file_path)

            ok = True

        return ok

    def load_models(self):
        """
        Load face models

        :rtype: boolean
        :returns: True if models were successfully loaded,
                  False otherwise
        """

        ok = False

        if self._ext_models:
            # Load external models
            self._loaded_ext_models = []
            for model_dict in self._ext_models:
                model_id = model_dict[c.MODEL_ID_KEY]
                db_file_path = model_dict[c.MODEL_FILE_KEY]
                face_recognizer = cv2.createLBPHFaceRecognizer()
                face_recognizer.load(db_file_path)
                tag = model_dict[c.TAG_KEY]
                loaded_model_dict = {c.MODEL_ID_KEY: model_id,
                                     c.MODEL_FILE_KEY: face_recognizer,
                                     c.TAG_KEY: tag}
                self._loaded_ext_models.append(loaded_model_dict)
                ok = True

        else:
            # Load internal models
            db_file_path = os.path.join(
                self._data_dir_path, c.FACE_MODELS_FILE)

            # Load face recognizer

            if os.path.exists(db_file_path):
                self._models = cv2.createLBPHFaceRecognizer()

                self._models.load(db_file_path)

                ok = True

        return ok

    def recognize_face(self, face):
        """
        Recognize given face using
        the stored face recognition models

        :type face: OpenCV image
        :param face: face to be recognized

        :rtype: tuple
        :returns: a tuple containing predicted label
                  and corresponding confidence
        """

        # Set parameters
        face_rec_threshold = c.GLOBAL_FACE_REC_THRESHOLD
        radius = c.LBP_RADIUS
        neighbors = c.LBP_NEIGHBORS
        grid_x = c.LBP_GRID_X
        grid_y = c.LBP_GRID_Y
        if c.GLOBAL_FACE_REC_THRESHOLD_KEY in self._params:
            face_rec_threshold = self._params[c.GLOBAL_FACE_REC_THRESHOLD_KEY]
        if c.LBP_RADIUS_KEY in self._params:
            radius = self._params[c.LBP_RADIUS_KEY]
        if c.LBP_NEIGHBORS_KEY in self._params:
            neighbors = self._params[c.LBP_NEIGHBORS_KEY]
        if c.LBP_GRID_X_KEY in self._params:
            grid_x = self._params[c.LBP_GRID_X_KEY]
        if c.LBP_GRID_Y_KEY in self._params:
            grid_y = self._params[c.LBP_GRID_Y_KEY]

        label = c.UNDEFINED_LABEL
        conf = sys.maxint

        # Create face recognizer and train it with given face
        query_model = cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)

        query_model.train(
            np.asarray([np.asarray(face, dtype=np.uint8)]),
            np.asarray([0]))

        if self._loaded_ext_models:

            # Get histograms from given model
            query_model_hists = query_model.getMatVector("histograms")

            query_hist = query_model_hists[0][0]

            for train_model_dict in self._loaded_ext_models:

                # Get histograms from train model
                train_model = train_model_dict[c.MODEL_FILE_KEY]
                train_model_hists = train_model.getMatVector("histograms")
                train_model_id = train_model_dict[c.MODEL_ID_KEY]

                # Iterate through LBP histograms
                # in training model
                for t in range(0, len(train_model_hists)):
                    train_hist = train_model_hists[t][0]
                    diff = cv2.compareHist(
                        query_hist, train_hist, cv.CV_COMP_CHISQR)
                    if ((diff < conf)and
                            (diff < face_rec_threshold)):
                        conf = diff
                        label = train_model_id

        elif self._en_models:

            # Get histograms from given face
            query_model_hists = query_model.getMatVector("histograms")

            query_hist = query_model_hists[0][0]

            # Get histograms from train model
            train_model_hists = self._en_models.getMatVector("histograms")
            train_model_labels = self._en_models.getMat("labels")

            # Iterate through LBP histograms
            # in training model
            for t in range(0, len(train_model_hists)):
                train_hist = train_model_hists[t][0]
                diff = cv2.compareHist(
                    query_hist, train_hist, cv.CV_COMP_CHISQR)
                if ((diff < conf) and
                        (diff < face_rec_threshold)):
                    conf = diff
                    label = train_model_labels[t][0]

        return label, conf

    def recognize_model(self, query_model):
        """
        Recognize given face model using the stored face recognition models

        :type query_model: LBPHFaceRecognizer
        :param query_model: model to be recognized

        :rtype: list
        :returns: a list of dictionaries containing, for each item in model,
                  predicted label and corresponding confidence.
                  Example:
                  results = [{'assigned_tag': 'Barack Obama', 'confidence': 60},
                             {'assigned_tag': 'Betty White', 'confidence': 30}
                            ]
        """

        face_rec_results = []

        # Set parameters
        face_rec_threshold = c.GLOBAL_FACE_REC_THRESHOLD
        if c.GLOBAL_FACE_REC_THRESHOLD_KEY in self._params:
            face_rec_threshold = self._params[c.GLOBAL_FACE_REC_THRESHOLD_KEY]

        if self._loaded_ext_models:

            # Get histograms from given model
            query_model_hists = query_model.getMatVector("histograms")

            # Iterate through LBP histograms
            # in query model
            for i in range(0, len(query_model_hists)):

                label = c.UNDEFINED_LABEL
                conf = sys.maxint

                query_hist = query_model_hists[i][0]

                for train_model_dict in self._loaded_ext_models:

                    # Get histograms from train model
                    train_model = train_model_dict[c.MODEL_FILE_KEY]
                    train_model_hists = train_model.getMatVector("histograms")
                    train_model_id = train_model_dict[c.MODEL_ID_KEY]

                    # Iterate through LBP histograms
                    # in training model
                    for t in range(0, len(train_model_hists)):
                        train_hist = train_model_hists[t][0]
                        diff = cv2.compareHist(
                            query_hist, train_hist, cv.CV_COMP_CHISQR)
                        if ((diff < conf)and
                                (diff < face_rec_threshold)):
                            conf = diff
                            label = train_model_id

                face_rec_result = {c.ASSIGNED_TAG_KEY: label,
                                   c.CONFIDENCE_KEY: conf
                                   }
                face_rec_results.append(face_rec_result)

        elif self._en_models:

            # Get histograms from given model
            query_model_hists = query_model.getMatVector("histograms")

            # Iterate through LBP histograms
            # in query model
            for i in range(0, len(query_model_hists)):

                label = c.UNDEFINED_LABEL
                conf = sys.maxint

                query_hist = query_model_hists[i][0]

                # Get histograms from train model
                train_model_hists = self._en_models.getMatVector("histograms")
                train_model_labels = self._en_models.getMat("labels")

                # Iterate through LBP histograms
                # in training model
                for t in range(0, len(train_model_hists)):
                    train_hist = train_model_hists[t][0]
                    diff = cv2.compareHist(
                        query_hist, train_hist, cv.CV_COMP_CHISQR)
                    if ((diff < conf) and
                            (diff < face_rec_threshold)):
                        conf = diff
                        label = train_model_labels[t][0]

                face_rec_result = {c.ASSIGNED_TAG_KEY: label,
                                   c.CONFIDENCE_KEY: conf
                                   }
                face_rec_results.append(face_rec_result)

        return face_rec_results

    def remove_blacklist_item(self, item):
        """
        Remove given item from list of words that make
        the results of the caption recognition on a frame rejected

        :type item: string
        :param item: item to be removed from blacklist

        :rtype: boolean
        :returns: true if item has been removed from blacklist
        """

        blacklist_file_path = os.path.join(
            self._data_dir_path, c.WORD_BLACKLIST_FILE)

        blacklist = []
        if os.path.exists(blacklist_file_path):
            blacklist = utils.load_YAML_file(blacklist_file_path)

        if item in blacklist:
            blacklist.remove(item)

        utils.save_YAML_file(blacklist_file_path, blacklist)

    def remove_face(self, label, im_name):
        """
        Remove face from face models

        :type label: integer
        :param label: label of person whom face belong to

        :type im_name: string
        :param im_name: name of image file containing the face

        :rtype: boolean
        :returns: true if face has been removed
        """

        ok = False

        rel_im_path = os.path.join(str(label), im_name)

        training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)

        aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)

        aligned_face_path = os.path.join(
            aligned_faces_path, rel_im_path)

        if os.path.exists(aligned_face_path):

            images_nr = self.get_images_nr_for_label(label)

            if images_nr == 1:

                # Remove tag

                ok = self.remove_label(label)

            else:

                try:

                    # Remove whole image
                    whole_images_path = os.path.join(
                        training_set_path, c.WHOLE_IMAGES_DIR)

                    whole_image_path = os.path.join(
                        whole_images_path, rel_im_path)

                    if os.path.exists(whole_image_path):
                        os.remove(whole_image_path)

                    # TEST ONLY remove bbox image
                    bbox_images_path = os.path.join(
                        training_set_path, c.BBOX_IMAGES_DIR)

                    bbox_image_path = os.path.join(
                        bbox_images_path, rel_im_path)

                    if os.path.exists(bbox_image_path):
                        os.remove(bbox_image_path)

                    # Remove aligned face

                    os.remove(aligned_face_path)

                    # Load file with faces
                    faces_file = os.path.join(
                        self._data_dir_path, c.FACES_FILE)
                    faces_dict = utils.load_YAML_file(faces_file)

                    if faces_dict:
                        for key in faces_dict.keys():
                            if key == rel_im_path:
                                del faces_dict[key]

                                # Save new dictionary in YAML file
                        utils.save_YAML_file(faces_file, faces_dict)

                    # Re-build the models
                    self.create_models_from_aligned_faces()

                    ok = True

                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise

        return ok

    def remove_label(self, label):
        """
        Remove label from face models

        :type label: integer
        :param label: label to be removed

        :rtype: boolean
        :returns: true if tag has been removed
        """

        ok = False

        # Convert label to string for use as directory name
        label_str = str(label)

        training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)

        # Remove directory with aligned faces related to tag

        aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)

        aligned_faces_subject_path = os.path.join(aligned_faces_path, label_str)

        if os.path.exists(aligned_faces_subject_path):

            try:

                # Remove directory with whole images related to tag                    
                whole_images_path = os.path.join(
                    training_set_path, c.WHOLE_IMAGES_DIR)

                whole_images_subject_path = os.path.join(
                    whole_images_path, label_str)

                if os.path.exists(whole_images_subject_path):
                    shutil.rmtree(whole_images_subject_path)

                # TEST ONLY remove directory with bbox images related to tag

                bbox_images_path = os.path.join(
                    training_set_path, c.BBOX_IMAGES_DIR)

                bbox_images_subject_path = os.path.join(
                    bbox_images_path, label_str)

                if os.path.exists(bbox_images_subject_path):
                    shutil.rmtree(bbox_images_subject_path)

                shutil.rmtree(aligned_faces_subject_path)

                # Load file with tag-label associations
                tag_label_associations_file = os.path.join(
                    self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
                tag_label_associations = utils.load_YAML_file(
                    tag_label_associations_file)

                if tag_label_associations:
                    # Remove label from dictionary
                    tag_label_associations.pop(label, None)

                    # Save new dictionary in YAML file
                    utils.save_YAML_file(
                        tag_label_associations_file, tag_label_associations)

                # Load file with faces
                faces_file = os.path.join(
                    self._data_dir_path, c.FACES_FILE)
                faces_dict = utils.load_YAML_file(faces_file)

                if faces_dict:

                    for key in faces_dict.keys():
                        key_label = os.path.split(key)[0]
                        if key_label == label:
                            del faces_dict[key]

                            # Save new dictionary in YAML file
                    utils.save_YAML_file(faces_file, faces_dict)

                # Re-build the models
                self.create_models_from_aligned_faces()

                ok = True

            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise

        return ok
