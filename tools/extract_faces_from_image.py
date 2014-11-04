import cv2
import os
from face_extractor import FaceExtractor
from Constants import ERROR_KEY, FACES_KEY, ASSIGNED_TAG_KEY, BBOX_KEY

def extract_faces(image_path):

    fe = FaceExtractor(None);

    handle = fe.extractFacesFromImage(image_path);

    result = fe.getResults(handle);
    
    error = result[ERROR_KEY];

    if(not(error)):

        image = cv2.imread(image_path, cv2.IMREAD_COLOR);

        faces = result[FACES_KEY];

        if(len(faces) == 0):

            cv2.putText(image,'Nessuna faccia rilevata', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

        else:

            for face in faces:

                tag = face[ASSIGNED_TAG_KEY];
            
                face_bbox = face[BBOX_KEY];
                x = face_bbox[0];
                y = face_bbox[1];
                w = face_bbox[2];
                h = face_bbox[3];
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0);

                cv2.putText(image,tag, (x,y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

        cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE);
        cv2.imshow('Result', image);
        cv2.waitKey(0); 

#subject_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\data\YouTube\Dataset_50\Test_set_1fps\Alonso_Fernando'

#for training_im in os.listdir(subject_path):
            
    #training_im_path = os.path.join(subject_path, training_im)

    #extract_faces(training_im_path)
 

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Extract faces from given image')

    parser.add_argument('image_path', metavar = 'image_path',
                        help = 'image path');
    args = parser.parse_args()
    
    image_path = args.image_path;
    
    extract_faces(image_path)
    
#image_path = r'C:\Active\Dataset\Videolina - Fotogrammi non annotati\People\fic.02\Paolo Fadda.jpg'

#extract_faces(image_path)

