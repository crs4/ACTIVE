import cv2
import sys
import yaml
import numpy as np
import os
from Constants import *

def read_images(path, sz=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.

    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes

    Returns:
        A list [X,y]

            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
    """
    c = 0
    X,y = [], []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,y]

def load_YAML_file(file_path):
    """Load YAML file.

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A dictionary with the contents of the file
    """
    with open(file_path, 'r') as stream:
        data = yaml.load(stream);
        return data;

def load_image_annotations(file_path):
    """Load YAML file with image .

    Args:
        file_path = path of YAML file to be loaded

    Returns:
        A list of dictionaries with the annotated images
    """
    data = load_YAML_file(file_path);

    images = data[ANNOTATIONS_FRAMES_KEY];
    return images;

def save_YAML_file(file_path, dictionary):
    """Save YAML file.

    Args:
        file_path = path of YAML file to be saved
        dictionary = dictionary with data to be saved

    Returns:
        A boolean indicating the result of the write operation
    """
    stream = open(file_path, 'w');
    result = stream.write(yaml.dump(dictionary, default_flow_style = False));
    stream.close();
    return result;

# Load file with results of all experiments and return list of experiments
def load_experiment_results(filePath):
    data = load_YAML_file(filePath);
    experiments = data[EXPERIMENTS_KEY];
    return experiments

