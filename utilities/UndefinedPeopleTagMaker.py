# This script adds to a YAML annotation file "Undefined" person name for those faces where no person name is present 

import sys
sys.path.append('..');
from tools.Constants import *
from tools.Utils import load_image_annotations, save_YAML_file

annotations_file_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face extraction\Annotations\fic.02_annotations.yml'

images = load_image_annotations(annotations_file_path);

for image in images:

    image_inner_dict = image[ANNOTATIONS_FRAME_KEY];

    imageName = image_inner_dict[ANNOTATIONS_FRAME_NAME_KEY];

    faces = image_inner_dict.get(ANNOTATIONS_FACES_KEY, 'undefined');

    if(faces == 'undefined'):
        continue;
    else:
        for face in faces:

            face_inner_dict = face[ANNOTATIONS_FACE_KEY];

            face_inner_dict[ANNOTATIONS_PERSON_TAG_KEY] = 0; # TEST ONLY

            personName = face_inner_dict.get(ANNOTATIONS_PERSON_NAME_KEY, 'undefined');

            if(personName == 'undefined'):

                face_inner_dict[ANNOTATIONS_PERSON_NAME_KEY] = 'Undefined';

annotationsDict = {};

annotationsDict[ANNOTATIONS_FRAMES_KEY] = images;

save_YAML_file(annotations_file_path, annotationsDict);


