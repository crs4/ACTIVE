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
    The persistent data structure containing the global face models
    used by the face recognition algorithm
    """

    def __init__(self, params=None):
        """
        Initialize the face models

        :type params: dictionary
        :param params: configuration parameters
        """

        self._params = params
        self._data_dir_path = c.GLOBAL_FACE_REC_DATA_DIR_PATH
        self._models = None

        # Association between tags 

        if params is not None:

            if c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY in params:
                self._data_dir_path = params[
                    c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY]

    def add_face(self, label, tag, im_path, aligned_face=None, eye_pos=None,
                 bbox=None):
        """
        Add face to face models

        :type label: integer
        :param label: identifier of person in database

        :type tag: string
        :param tag: tag of person whom face belong to

        :type im_path: string
        :param im_path: path of image containing the face

        :type aligned_face: OpenCV image
        :param aligned_face: aligned face

        :type eye_pos: tuple
        :param eye_pos: tuple containing eye positions
        (left_eye_x, left_eye_y, right_eye_x, right_eye_y)

        :type bbox: tuple
        :param bbox: tuple containing position and size of
        face bounding box in whole image (x, y, width, height)

        :rtype: boolean
        :returns: true if face has been added
        """

        ok = False

        try:

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

            # TEST ONLY
            # print('im_path', im_path)
            # print('eye_pos', eye_pos)
            # print('bbox', bbox)
            # cv2.imshow('aligned_face', aligned_face)
            # cv2.waitKey(0)

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

                    if ((len(faces) == 1) and (c.FACE_KEY in faces[0]) and
                            (c.BBOX_KEY in faces[0]) and
                            (c.LEFT_EYE_POS_KEY in faces[0]) and
                            (c.RIGHT_EYE_POS_KEY in faces[0])):

                        aligned_face = faces[0][c.FACE_KEY]

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

                aligned_im_path = os.path.join(aligned_faces_subject_path, im_name)

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

                # TODO DELETE (TEST ONLY) Save whole image with face bbox
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
                            (c.GLOBAL_FACE_MODELS_MIN_DIFF in self._params)):
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

                    # Create models

                    # Create face recognizer
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

                    model = cv2.createLBPHFaceRecognizer(
                        radius,
                        neighbors,
                        grid_x,
                        grid_y)

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

                faces_dict[rel_im_path][c.LEFT_EYE_POS_KEY] = eye_right

                faces_dict[rel_im_path][c.FACE_IN_MODELS_KEY] = face_in_models

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

        :rtype boolean
        :returns: true if item has been added to blacklist
        """

        blacklist_file_path = os.path.join(
            self._data_dir_path, c.WORD_BLACKLIST_FILE)

        blacklist = self.get_blacklist()

        if item not in blacklist:
            blacklist.append(item)

        utils.save_YAML_file(blacklist_file_path, blacklist)

    # TODO REVIEW
    def create_models_from_aligned_faces(self):
        """
        Read images in directory with aligned faces and create face models.
        Directory with aligned faces must contain
        one sub directory for each person.
        """

        training_set_path = os.path.join(
            self._data_dir_path, c.TRAINING_SET_DIR)

        aligned_faces_path = os.path.join(
            training_set_path, c.ALIGNED_FACES_DIR)

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

        model = cv2.createLBPHFaceRecognizer(
            radius,
            neighbors,
            grid_x,
            grid_y)

        tag_label_associations = {}

        # Load file with faces
        faces_file = os.path.join(
            self._data_dir_path, c.FACES_FILE)
        faces_dict = utils.load_YAML_file(faces_file)
        if faces_dict is None:
            # Create dictionary with face data
            faces_dict = {}

        im_counter = 0
        subject_counter = 0

        for sub_dir_name in os.listdir(aligned_faces_path):

            tag_label_associations[subject_counter] = sub_dir_name

            subject_path = os.path.join(
                aligned_faces_path, sub_dir_name)

            for im_name in os.listdir(subject_path):

                im_path = os.path.join(subject_path, im_name)

                rel_im_path = os.path.join(sub_dir_name, im_name)

                if rel_im_path not in faces_dict:
                    faces_dict[rel_im_path] = {}

                face_in_models = False

                try:

                    face = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

                    # If this is the first image train model,
                    # otherwise update it

                    if im_counter == 0:

                        model.train(
                            np.asarray([np.asarray(face, dtype=np.uint8)]),
                            np.asarray(subject_counter))

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
                                    np.asarray(subject_counter))

                                face_in_models = True

                        else:

                            model.update(
                                np.asarray([np.asarray(face, dtype=np.uint8)]),
                                np.asarray(subject_counter))

                            face_in_models = True

                    faces_dict[rel_im_path][
                        c.FACE_IN_MODELS_KEY] = face_in_models

                    im_counter += 1

                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise

            subject_counter += 1


        # Save file with face models
        db_file_name = os.path.join(
            self._data_dir_path, c.FACE_MODELS_FILE)

        model.save(db_file_name)

        self._models = model

        # Save file with tag-label associations
        tag_label_associations_file = os.path.join(
            self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        utils.save_YAML_file(
            tag_label_associations_file, tag_label_associations)

        # Save new dictionary in YAML file
        utils.save_YAML_file(faces_file, faces_dict)

    def create_models_from_whole_images(self, images_dir_path):
        """
        Read images in given directory with images,
        detect and align faces in them and create face models.
        Directory with whole images must contain
        one sub directory for each person.

        :type images_dir_path: string
        :param images_dir_path: path of directory with images of people

        :rtype: integer
        :returns: number of faces added to models
        """

        # Remove existing directories and files

        added_faces = 0

        try:

            # Remove existing data
            self.delete_models()

            # Iterate through sub directories with images of people
            subject_counter = 0  # Used as label for person

            for sub_dir_name in os.listdir(images_dir_path):

                # TEST ONLY
                print 'Creating models for ' + sub_dir_name

                subject_path = os.path.join(images_dir_path, sub_dir_name)

                for im_name in os.listdir(subject_path):

                    im_path = os.path.join(subject_path, im_name)

                    # Add image to face models
                    ok = self.add_face(subject_counter, sub_dir_name, im_path)

                    if ok:
                        added_faces += 1

                subject_counter += 1

        except IOError, (errno, strerror):

            print "I/O error({0}): {1}".format(errno, strerror)

        except:

            print "Unexpected error:", sys.exc_info()[0]
            raise

        return added_faces

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

    def get_labels(self):
        """
        Get all labels

        :rtype: set
        :returns: a set containing all labels
        """

        labels = []

        # Load file with tag-label associations
        tag_label_associations_file = os.path.join(
            self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        tag_label_associations = utils.load_YAML_file(
            tag_label_associations_file, )

        if tag_label_associations:
            labels = tag_label_associations.keys()

        return set(labels)

    def get_labels_for_tag(self, tag):
        """
        Get label corresponding to given tag

        :type tag: string
        :param tag: tag for which corresponding label is wanted

        :rtype: list
        :returns: list of labels corresponding to given tag
        """

        labels = []

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

        # Load file with tag-label associations
        tag_label_associations_file = os.path.join(
            self._data_dir_path, c.TAG_LABEL_ASSOCIATIONS_FILE)
        tag_label_associations = utils.load_YAML_file(
            tag_label_associations_file, )

        if tag_label_associations:
            tags = tag_label_associations.values()

        return set(tags)

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

    def load_models(self):
        """
        Load face models

        :rtype: boolean
        :returns: True if models were successfully loaded,
        False otherwise
        """

        ok = False

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
        and relative confidence
        """

        label = c.UNDEFINED_TAG
        conf = sys.maxint

        if self._models:

            (pred_label, conf) = self._models.predict(
                np.asarray(face, dtype=np.uint8))
            # TEST ONLY
            print('pred_label', pred_label)
            print('conf', conf)
            cv2.imshow('face', face)
            cv2.waitKey(0)

            # Consider tag only if distance is below threshold
            if conf < c.GLOBAL_FACE_REC_THRESHOLD:
                label = pred_label

        return label, conf

    def remove_blacklist_item(self, item):
        """
        Remove given item from list of words that make
        the results of the caption recognition on a frame rejected

        :type item: string
        :param item: item to be removed from blacklist

        :rtype boolean
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
                    self.create_models()

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
                self.create_models()

                ok = True

            except IOError, (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise

        return ok
