import cv2

from face_extractor import FaceExtractor
from Constants import FACE_EXTRACTION_ERROR_KEY, FACE_EXTRACTION_FACES_KEY, FACE_EXTRACTION_TAG_KEY, FACE_EXTRACTION_BBOX_KEY

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Extract faces from given image')

    parser.add_argument('image_path', metavar = 'image_path',
                        help = 'image path');
    args = parser.parse_args()
    
    image_path = args.image_path;

    fe = FaceExtractor(None);

    handle = fe.extractFacesFromImage(image_path);

    result = fe.getResults(handle);

    error = result[FACE_EXTRACTION_ERROR_KEY];

    if(len(error) == 0):

        image = cv2.imread(image_path, cv2.IMREAD_COLOR);

        faces = result[FACE_EXTRACTION_FACES_KEY];

        for face in faces:

            tag = face[FACE_EXTRACTION_TAG_KEY];
        
            face_bbox = face[FACE_EXTRACTION_BBOX_KEY];
            x = face_bbox[0];
            y = face_bbox[1];
            w = face_bbox[2];
            h = face_bbox[3];
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 3, 8, 0);

            cv2.putText(image,tag, (x+w,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)

        cv2.namedWindow('Result', cv2.WINDOW_NORMAL);
        cv2.imshow('Result', image);
        cv2.waitKey(0);
