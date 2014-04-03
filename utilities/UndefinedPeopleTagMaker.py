# This script adds to a YAML annotation file "Undefined" person name for those faces where no person name is present 

from Utils import *
import Constants

annotationFilePath = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\Annotations\fic.15_annotations.yml'

images = loadFrameAnnotations(annotationFilePath);

for image in images:

    imageInnerDict = image[ANNOTATIONS_FRAME_KEY];

    imageName = imageInnerDict[ANNOTATIONS_FRAME_NAME_KEY];

    faces = imageInnerDict.get(ANNOTATIONS_FACES_KEY, 'undefined');

    if(faces == 'undefined'):
        continue;
    else:
        for face in faces:

            faceInnerDict = face[ANNOTATIONS_FACE_KEY];

            personName = faceInnerDict.get(ANNOTATATIONS_PERSON_NAME_KEY, 'undefined');

            if(personName == 'undefined'):

                faceInnerDict[ANNOTATATIONS_PERSON_NAME_KEY] = 'Undefined';

annotationsDict = {};

#annotationsDict[ANNOTATIONS_FRAMES_KEY] = images;

#saveYAMLFile(annotationFilePath, annotationsDict);


