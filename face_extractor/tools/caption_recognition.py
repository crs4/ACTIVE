import argparse
import constants as c
import cv2
import cv2.cv as cv
import Levenshtein as Lev
import numpy as np
import sys
import tesseract
from face_models import FaceModels
from utils import load_YAML_file, save_YAML_file
from itertools import permutations


def check_permutations(max_lev_ratio, label_parts, words):
    """
    Check permutations of label parts

    :type max_lev_ratio: float
    :param max_lev_ratio: previous maximum Levenshtein ratio

    :type label_parts: list
    :param label_parts: parts in which label is divided

    :type words: list
    :param words: words found in analyzed image portion

    :rtype: float
    :returns: maximum Levenshtein ratio
    """

    label_parts_nr = len(label_parts)

    perms = [''.join(p) for p in permutations(label_parts)]

    for perm in perms:

        for word in words:

            word_lev_ratio = Lev.ratio(perm.lower(), word.lower())

            w_word_lev_ratio = word_lev_ratio * label_parts_nr

            if w_word_lev_ratio > max_lev_ratio:
                max_lev_ratio = w_word_lev_ratio

    return max_lev_ratio


def find_letters_in_image(gray_im, api, use_max_height, show_image):
    """
    Find letters in given image

    :type gray_im: OpenCV image
    :param gray_im: image to be analyzed

    :type api: TessBaseAPI
    :param api: api used by tesseract

    :type use_max_height: boolean
    :param use_max_height: if True, discards contours that are too high

    :type show_image: boolean
    :param show_image: if True, show image with black and white caption block

    :rtype: dictionary
    :returns: dictionary with results (see table)

    =====================================  =====================================
    Key                                    Value
    =====================================  =====================================
    all_letters                            List of found letters
    contours                               List of found contours
    hierarchy                              Contour hierarchy
    ord_bboxs                              Contour bounding boxes
                                           ordered from left to right
    ord_contour_idxs                       Indexes of ordered contours
    =====================================  =====================================
    """

    result_dict = {}

    im_height, im_width = gray_im.shape

    # Convert grayscale image to black and white image

    flags = cv2.THRESH_BINARY | cv2.THRESH_OTSU
    th, bw_im = cv2.threshold(gray_im, 128, 255, flags)

    # Find contours in image
    mode = cv2.RETR_TREE
    method = cv2.CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(bw_im, mode, method)

    result_dict[c.CONTOURS_KEY] = contours
    result_dict[c.HIERARCHY_KEY] = hierarchy

    # Order contours from left to right
    bbox_xs = []
    bboxs = []
    contour_idx = 0

    for contour in contours:
        bbox = cv2.boundingRect(contour)
        x1 = bbox[0]
        y1 = bbox[1]

        bbox_xs.append(x1)
        bboxs.append(bbox)

    idxs = [i[0] for i in sorted(enumerate(bbox_xs), key=lambda x: x[1])]

    useful_contour_counter = 0
    all_letters = []
    all_letters_str = ''

    ord_bboxs = []
    ord_contour_idxs = []

    for idx in idxs:

        bbox = bboxs[idx]
        x1 = bbox[0]
        y1 = bbox[1]
        w = bbox[2]
        h = bbox[3]
        x2 = x1 + w
        y2 = y1 + h

        if h < c.MIN_CHAR_HEIGHT:
            continue

        if use_max_height:
            if h > (c.MAX_CHAR_HEIGHT_PCT * im_height):
                continue

        if w > (c.MAX_CHAR_WIDTH_PCT * im_width):
            continue

        ord_bboxs.append(bbox)
        ord_contour_idxs.append(idx)

        bw_im[:, :] = 255

        cv2.drawContours(bw_im, contours, idx, 0, -1, cv2.CV_AA, hierarchy, 1)

        if show_image:
            cv2.imshow('bw_im inside', bw_im)
            cv2.waitKey(0)

        lett_im = cv2.copyMakeBorder(bw_im[y1:y2, x1:x2], c.LETT_MARGIN,
                                     c.LETT_MARGIN, c.LETT_MARGIN,
                                     c.LETT_MARGIN, cv2.BORDER_CONSTANT,
                                     value=255)

        text = ''
        kernel_size = 0
        or_lett_im = lett_im.copy()
        while (len(text) == 0) and (kernel_size <= c.KERNEL_MAX_SIZE):

            # Dilate image
            if kernel_size > 0:
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                lett_im = cv2.dilate(or_lett_im, kernel)

            kernel_size += 1
            shape_1 = lett_im.shape[1]
            shape_0 = lett_im.shape[0]
            depth = cv.IPL_DEPTH_8U
            bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
            cv.SetData(bitmap, lett_im.tostring(),
                       lett_im.dtype.itemsize * 1 * shape_1)

            tesseract.SetCvImage(bitmap, api)
            text = api.GetUTF8Text().rstrip()

        # Try to identify char by adding to image a known char
        if len(text) == 0:
            lett_im = cv2.copyMakeBorder(bw_im[y1:y2, x1:x2], c.LETT_MARGIN,
                                         c.LETT_MARGIN, c.LETT_MARGIN,
                                         3 * c.LETT_MARGIN + h,
                                         cv2.BORDER_CONSTANT, value=255)
            text_size = h / c.PELS_TO_TEXT_SIZE_RATIO
            cv2.putText(lett_im, 'B', (w + c.LETT_MARGIN * 2, h),
                        cv2.FONT_HERSHEY_SIMPLEX, text_size, 0, 2)

            # Transform image
            shape_1 = lett_im.shape[1]
            shape_0 = lett_im.shape[0]
            depth = cv.IPL_DEPTH_8U
            bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
            cv.SetData(bitmap, lett_im.tostring(),
                       lett_im.dtype.itemsize * 1 * shape_1)

            api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
            tesseract.SetCvImage(bitmap, api)
            text = api.GetUTF8Text().rstrip()
            api.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)

            if len(text) == 2:
                text = text[0]

        all_letters_str = all_letters_str + text
        all_letters.append(text)

        useful_contour_counter += 1

    result_dict[c.ALL_LETTERS_KEY] = all_letters
    result_dict[c.ORD_BBOXS_KEY] = ord_bboxs
    result_dict[c.ORD_CONTOUR_IDXS_KEY] = ord_contour_idxs

    return result_dict

def find_most_similar_tag(tags, words, params=None):
    """
    Find tag in tag dictionary that is most similar to words found in image

    :type tags: set
    :param tags: set of tags in dictionary

    :type words: list
    :param words: list of words found in image

    :type params: dictionary
    :param params: configuration parameters to be used
                   for the caption recognition (see table)

    :rtype: dictionary
    :returns: dictionary with results

    ============================================  ========================================  ==============
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  ==============
    lev_ratio_pct_threshold                       Minimum threshold for considering         0.8
                                                  captions in frame
    min_tag_length                                Minimum length of tags considered         10
                                                  in caption recognition
    use_levenshtein                               If True, words found in image             True
                                                  by caption recognition and tags
                                                  are compared by using
                                                  the Levenshtein distance
    ============================================  ========================================  ==============

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    assigned_tag                           Predicted tag (most similar tag)
    eq_letters_nr                          Similarity value for most similar tag
                                           (not normalized)
    tot_letters_nr                         Maximum possible similarity value
    confidence                             Confidence associated to prediction
                                           (normalized similarity value)
    tags                                   Set of tags in dictionary
    =====================================  =====================================
    """
    # Get values from params
    use_levenshtein = c.USE_LEVENSHTEIN
    lev_thresh = c.LEV_RATIO_PCT_THRESH
    min_tag_length = c.MIN_TAG_LENGTH

    if params is not None:
        if c.USE_LEVENSHTEIN_KEY in params:
            use_levenshtein = params[c.USE_LEVENSHTEIN_KEY]
        if c.LEV_RATIO_PCT_THRESH_KEY in params:
            lev_thresh = params[c.LEV_RATIO_PCT_THRESH_KEY]
        if c.MIN_TAG_LENGTH_KEY in params:
            min_tag_length = params[c.MIN_TAG_LENGTH_KEY]

    assigned_tag = c.UNDEFINED_TAG
    eq_letters_nr = 0
    tot_letters_nr = 0
    lett_counter_list = []
    tag_parts_len_list = []
    lett_pct_list = []
    label = 0
    tags = list(tags)
    considered_tags = []  # Tags that have a sufficient number of characters

    for tag in tags:

        # Divide name(s) and surname(s)
        tag_parts = tag.split(c.TAG_SEP)

        # Skip tags that are too short
        tot_len = 0
        for tag_part in tag_parts:
            tot_len += len(tag_part)

        if tot_len < min_tag_length:
            continue
        else:
            considered_tags.append(tag)

        lett_counter = 0
        tag_parts_len = 0
        tag_parts_nr = len(tag_parts)

        for tag_part in tag_parts:
            tag_parts_len += len(tag_part)

            # Consider each word separately
            word_lett_counter_l = []

            complete_check_found = False
            for word in words:

                # Index of letters that must not be considered anymore

                if use_levenshtein:

                    word_lev_ratio = Lev.ratio(tag_part.lower(),
                                               word.lower())

                    if word_lev_ratio == 1:
                        lett_counter = lett_counter + word_lev_ratio

                        complete_check_found = True

                    word_lett_counter_l.append(word_lev_ratio)

                else:

                    black_list = []
                    word_lett_counter = 0
                    start = 0

                    for i in range(0, len(tag_part)):

                        # For each letter in tag part
                        lett = tag_part[i]

                        lett_idx = word.lower().find(lett.lower(), start)

                        if ((lett_idx != -1) and
                                (lett_idx not in black_list)):
                            word_lett_counter += 1
                            start = lett_idx + 1
                            black_list.append(lett_idx)

                        if word_lett_counter == len(tag_part):
                            lett_counter += word_lett_counter
                            complete_check_found = True

                    word_lett_counter_l.append(word_lett_counter)

                if complete_check_found:
                    break  # Do not consider other words

            # Add to total best row check
            if not complete_check_found:

                if len(word_lett_counter_l) > 0:
                    lett_counter = lett_counter + max(word_lett_counter_l)

        if use_levenshtein:

            if lett_counter == tag_parts_nr:

                assigned_tag = tag
                eq_letters_nr = lett_counter
                tot_letters_nr = lett_counter
                break

            else:

                # Check also permutations of tag parts
                lett_counter = check_permutations(lett_counter, tag_parts,
                                                  words)

                lett_counter_list.append(lett_counter)
                tag_parts_len_list.append(tag_parts_nr)
                lev_ratio_pct = lett_counter / tag_parts_nr
                lett_pct_list.append(lev_ratio_pct)

        else:

            if lett_counter == tag_parts_len:

                assigned_tag = tag
                eq_letters_nr = lett_counter
                tot_letters_nr = lett_counter
                break

            else:

                lett_counter_list.append(lett_counter)
                tag_parts_len_list.append(tag_parts_len)
                lett_pct = float(lett_counter) / tag_parts_len
                lett_pct_list.append(lett_pct)

        label += 1

    # Find more probable tag
    if assigned_tag == c.UNDEFINED_TAG:

        tag_idxs = [i[0] for i in sorted(enumerate(lett_pct_list),
                                         key=lambda x: x[1], reverse=True)]
        assigned_label = tag_idxs[0]
        # Get final tag, taking into account skipped tags
        assigned_tag = considered_tags[assigned_label]
        eq_letters_nr = lett_counter_list[assigned_label]
        tot_letters_nr = tag_parts_len_list[assigned_label]

    # Do not consider recognitions below threshold
    lev_ratio_pct = 0
    if tot_letters_nr != 0:
        lev_ratio_pct = float(eq_letters_nr) / tot_letters_nr

    if lev_ratio_pct < lev_thresh:
        assigned_tag = c.UNDEFINED_TAG
    # TODO DELETE TEST ONLY
    # else:
    #     if use_levenshtein:
    #         print "Predicted tag = %s (Levenshtein ratio of %f on %f)" % (
    #             assigned_tag, eq_letters_nr, tot_letters_nr)
    #     else:
    #
    #         print "Predicted tag = %s (%d equal letters out of %d)" % (
    #             assigned_tag, eq_letters_nr, tot_letters_nr)

    result_dict = {c.ASSIGNED_TAG_KEY: assigned_tag,
                   c.EQ_LETTERS_NR_KEY: eq_letters_nr,
                   c.TOT_LETTERS_NR_KEY: tot_letters_nr,
                   c.CONFIDENCE_KEY: lev_ratio_pct, c.TAGS_KEY: tags}

    return result_dict


def get_tag_from_image(im_path, params=None, api=None):
    """
    Find tag in image captions

    :type im_path: string
    :param im_path: path of image to be analyzed

    :type params: dictionary
    :param params: configuration parameters to be used for
                   the caption recognition

    :type api: Tesseract TessBaseAPI
    :param api: api to be used for the Optical Character Recognition

    :rtype: dictionary
    :returns: dictionary with results (see table)

    ============================================  ========================================  ==============
    Key (params)                                  Value                                     Default value
    ============================================  ========================================  ==============
    lev_ratio_pct_threshold                       Minimum threshold for considering         0.8
                                                  captions in frame
    min_tag_length                                Minimum length of tags considered         10
                                                  in caption recognition
    tags_file_path                                Path of text file containing
                                                  list of tags
    tesseract_parent_dir_path                     Path of directory containing
                                                  'tesseract' directory
    use_blacklist                                 If True, use blacklist of items           True
                                                  that make the results of the
                                                  caption recognition on a frame
                                                  rejected
    use_levenshtein                               If True, words found in image             True
                                                  by caption recognition and tags
                                                  are compared by using
                                                  the Levenshtein distance
    ============================================  ========================================  ==============

    =====================================  =====================================
    Key (results)                          Value
    =====================================  =====================================
    assigned_tag                           Predicted tag (most similar tag)
    eq_letters_nr                          Similarity value for most similar tag
                                           (not normalized)
    tot_letters_nr                         Maximum possible similarity value
    confidence                             Confidence associated to prediction
                                           (normalized similarity value)
    tags                                   Set of tags in dictionary
    =====================================  =====================================
    """

    gray_im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

    if api is None:
        # Tesseract init
        api = tesseract.TessBaseAPI()

        # Set parent directory of "tessdata" directory
        tesseract_parent_dir_path = c.TESSERACT_PARENT_DIR_PATH
        if (params is not None) and (c.TESSERACT_PARENT_DIR_PATH_KEY in params):
            tesseract_parent_dir_path = params[c.TESSERACT_PARENT_DIR_PATH_KEY]

        api.Init(tesseract_parent_dir_path, "eng", tesseract.OEM_DEFAULT)

        api.SetVariable("tessedit_char_whitelist",
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        api.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)

    result_dict = find_letters_in_image(gray_im, api, True, False)

    contours = result_dict[c.CONTOURS_KEY]

    hierarchy = result_dict[c.HIERARCHY_KEY]

    all_letters = result_dict[c.ALL_LETTERS_KEY]

    ord_bboxs = result_dict[c.ORD_BBOXS_KEY]
    ord_contour_idxs = result_dict[c.ORD_CONTOUR_IDXS_KEY]

    # Divide letters by row
    rows = []
    rows_bboxs = []
    rows_contour_idxs = []
    # Index of letters that must not be considered anymore
    idx_black_list = []

    lett_idx = 0

    for lett in all_letters:
        if (lett_idx not in idx_black_list) and (len(lett) > 0):

            idx_black_list.append(lett_idx)
            bbox = ord_bboxs[lett_idx]
            x1 = bbox[0]
            y1 = bbox[1]
            w = bbox[2]
            h = bbox[3]
            y2 = y1 + h

            big_bbox = bbox

            row = [lett]
            row_bboxs = [bbox]

            contour_idx = ord_contour_idxs[lett_idx]
            row_contour_idxs = [contour_idx]

            pt1 = (bbox[0], bbox[1])

            for idx2 in range((lett_idx + 1), len(all_letters)):

                if idx2 not in idx_black_list:

                    lett2 = all_letters[idx2]
                    bbox2 = ord_bboxs[idx2]
                    x12 = bbox2[0]
                    y12 = bbox2[1]
                    w2 = bbox2[2]
                    h2 = bbox2[3]
                    x22 = x12 + w2
                    y22 = y12 + h2

                    if (((y12 > (y1 - c.MAX_BBOX_DIFF)) and (y12 < y2)) or
                            ((y22 > y1) and (y22 < (y2 + c.MAX_BBOX_DIFF)))):
                        lett2 = all_letters[idx2]
                        idx_black_list.append(idx2)

                        # Discard letter if it is inside previous letter
                        big_x = big_bbox[0]
                        big_y = big_bbox[1]
                        big_w = big_bbox[2]
                        big_h = big_bbox[3]
                        big_x2 = big_x + big_w
                        big_y2 = big_y + big_h

                        if (not ((x12 > big_x) and (y12 > big_y)
                                 and (x22 < big_x2) and (y22 < big_y2))):
                            row.append(lett2)

                            row_bboxs.append(bbox2)

                            contour_idx = ord_contour_idxs[idx2]

                            row_contour_idxs.append(contour_idx)

                            big_bbox = bbox2

            rows.append(row)
            rows_bboxs.append(row_bboxs)
            rows_contour_idxs.append(row_contour_idxs)

        lett_idx += 1

    im_height, im_width = gray_im.shape

    row_idx = 0
    words = []
    for row in rows:

        x1_min = im_width
        y1_min = im_height
        x2_max = 0
        y2_max = 0

        for i in range(0, len(row)):

            lett = row[i]

            contour_idx = rows_contour_idxs[row_idx][i]

            contour_bbox = rows_bboxs[row_idx][i]

            x1 = contour_bbox[0]
            y1 = contour_bbox[1]
            w = contour_bbox[2]
            h = contour_bbox[3]
            x2 = x1 + w
            y2 = y1 + h

            if x1 < x1_min:
                x1_min = x1
            if y1 < y1_min:
                y1_min = y1
            if x2 > x2_max:
                x2_max = x2
            if y2 > y2_max:
                y2_max = y2

        # Convert block region in original image to black and white image

        block_im = cv2.copyMakeBorder(
            gray_im[y1_min - c.LETT_MARGIN: y2_max + c.LETT_MARGIN,
            x1_min - c.LETT_MARGIN: x2_max + c.LETT_MARGIN],
            c.LETT_MARGIN, c.LETT_MARGIN, c.LETT_MARGIN, c.LETT_MARGIN,
            cv2.BORDER_CONSTANT, value=255)

        block_result_dict = find_letters_in_image(block_im, api, False, False)

        block_contours = block_result_dict[c.CONTOURS_KEY]

        block_hierarchy = block_result_dict[c.HIERARCHY_KEY]

        block_all_letters = block_result_dict[c.ALL_LETTERS_KEY]

        block_ord_bboxs = block_result_dict[c.ORD_BBOXS_KEY]

        block_ord_contour_idxs = block_result_dict[c.ORD_CONTOUR_IDXS_KEY]

        block_im[:, :] = 255

        is_first_lett = True

        big_bbox = None

        for i in range(0, len(block_all_letters)):

            lett = block_all_letters[i]

            if len(lett) > 0:

                if is_first_lett:
                    big_bbox = block_ord_bboxs[i]
                    is_first_lett = False

                else:

                    big_x = big_bbox[0]
                    big_y = big_bbox[1]
                    big_w = big_bbox[2]
                    big_h = big_bbox[3]
                    big_x2 = big_x + big_w
                    big_y2 = big_y + big_h

                    bbox = block_ord_bboxs[i]
                    x1 = bbox[0]
                    y1 = bbox[1]
                    w = bbox[2]
                    h = bbox[3]
                    x2 = x1 + w
                    y2 = y1 + h

                    # Discard letter if it is inside previous letter

                    if (not ((x1 > big_x) and (y1 > big_y)
                             and (x2 < big_x2) and (y2 < big_y2))):
                        contour_idx = block_ord_contour_idxs[i]

                        cv2.drawContours(block_im, block_contours,
                                         contour_idx, 0, -1, cv2.CV_AA,
                                         block_hierarchy, 1)

                        big_bbox = bbox

        # Transform image
        shape_1 = block_im.shape[1]
        shape_0 = block_im.shape[0]
        depth = cv.IPL_DEPTH_8U
        bitmap = cv.CreateImageHeader((shape_1, shape_0), depth, 1)
        cv.SetData(bitmap, block_im.tostring(),
                   block_im.dtype.itemsize * 1 * shape_1)

        api.SetPageSegMode(tesseract.PSM_SINGLE_BLOCK)
        tesseract.SetCvImage(bitmap, api)
        text = api.GetUTF8Text().rstrip()

        if len(text) > 0:
            row_words = text.split()
            for row_word in row_words:
                words.append(row_word)

        row_idx += 1

    tags = []
    use_blacklist = c.USE_BLACKLIST
    tags_file_path = None

    if params is not None:
        if c.USE_BLACKLIST_KEY in params:
            use_blacklist = params[c.USE_BLACKLIST_KEY]
        if c.TAGS_FILE_PATH_KEY in params:
            tags_file_path = params[c.TAGS_FILE_PATH_KEY]

    if tags_file_path:
        # Load tags from file
        tags = get_tags_from_file(tags_file_path)
    else:
        fm = FaceModels(params)
        tags = fm.get_tags()

    assigned_tag = c.UNDEFINED_TAG
    eq_letters_nr = 0
    tot_letters_nr = 0
    lev_ratio_pct = 0

    result_dict = {c.ASSIGNED_TAG_KEY: assigned_tag,
                   c.EQ_LETTERS_NR_KEY: eq_letters_nr,
                   c.TOT_LETTERS_NR_KEY: tot_letters_nr,
                   c.CONFIDENCE_KEY: lev_ratio_pct, c.TAGS_KEY: tags}

    blacklist_results = None
    if use_blacklist:
        # Check if one blacklist item is found in image
        blacklist = fm.get_blacklist()

        if len(blacklist) > 0:
            blacklist_results = find_most_similar_tag(blacklist, words, params)

    if ((blacklist_results is None) or
            (blacklist_results[c.ASSIGNED_TAG_KEY] == c.UNDEFINED_TAG)):
        if len(tags) > 0:
            result_dict = find_most_similar_tag(tags, words, params)

    # Save file with results
    caption_results_file_path = c.CAPTION_RESULTS_FILE_PATH
    if params is not None and c.CAPTION_RESULTS_FILE_PATH_KEY in params:
        caption_results_file_path = params[c.CAPTION_RESULTS_FILE_PATH_KEY]
    save_YAML_file(caption_results_file_path, result_dict)

    return result_dict

def get_tags_from_file(tags_file_path):
    """
    Get tags from text file

    :type tags_file_path: string
    :param tags_file_path: path of file with tags

    :rtype: list
    :returns: list of tags
    """

    with open(tags_file_path, 'r') as f:

        tags = f.read().splitlines()

    f.close()

    return tags


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Execute caption recognition on given image")
    parser.add_argument("-im_path", help="image path")
    parser.add_argument("-config", help="configuration file")

    args = parser.parse_args()

    im_path = None

    if args.im_path:
        im_path = args.im_path
    else:
        if im_path is None:
            print("Resource path not provided")
            exit()

    # Set parameters
    params = None

    if args.config:
        # Load given configuration file
        try:
            params = load_YAML_file(args.config)
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))
            print("Default configuration file will be used")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    else:
        print("Default configuration file will be used")

    get_tag_from_image(im_path, params)





