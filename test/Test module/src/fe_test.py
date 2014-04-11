from os import listdir, path
import cv2
import numpy
from sympy import Polygon
import sys
sys.path.append("../../..");
from tools.Constants import *
from tools.face_extractor import FaceExtractor
from tools.Utils import load_experiment_results,load_image_annotations, load_YAML_file, save_YAML_file

def fe_test(params, show_results):
    ''' Execute face extraction test

    :type params: dictionary
    :param params: dictionary containing the parameters to be used for the test

    :type show_results: boolean
    :param show_results: show (true) or do not show (false) image with detected and classified faces
    '''

    if(params == None):
        # Load default configuration file
        params = load_YAML_file(TEST_CONFIGURATION_FILE_PATH);

    fe_test_params = params[FACE_EXTRACTION_KEY];
    image_path = fe_test_params[SOFTWARE_TEST_FILE_KEY];

    test_passed = True;

    try:

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE);
        image_width = len(image[0,:]);
        image_height = len(image[:,0]);
        polygon_image = Polygon((0,0), (image_width, 0), (image_width, image_height), (0, image_height));        

        fe = FaceExtractor(None);

        result = fe.extract_faces_from_image_sync(image_path);

        error = result[FACE_EXTRACTION_ERROR_KEY];

        if(len(error) == 0):

            faces = result[FACE_EXTRACTION_FACES_KEY];
            
            for face in faces:
                
                label = face[FACE_EXTRACTION_TAG_KEY];
                # TO DO: CHECK THAT LABEL IS A POSSIBLE VALUE (E.G LABEL BETWEEN 0 AND 40)

                # Check that bounding box rectangle is inside the original image
                face_bbox = face[FACE_EXTRACTION_BBOX_KEY];
                x = face_bbox[0];
                y = face_bbox[1];
                width = face_bbox[2];
                height = face_bbox[3];

                polygon_bbox = Polygon((x,y), (x+width,y), (x+width, y+height), (x, y+height));
                if(not(polygon_image.encloses(polygon_bbox))):
                    test_passed = False;
                    break;
            
        else:
            test_passed = False;
        
    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror);
        test_passed = False;
    except:
        print "Unexpected error:", sys.exc_info()[0];
        test_passed = False;
        raise;
        
    return test_passed;

if __name__ == "__main__":
    
    import argparse
    
    parser = argparse.ArgumentParser(description = "Execute face extraction tests")
    parser.add_argument("-config", help = "configuration file");
    args = parser.parse_args()

    if(args.config):
        # Load given configuration file
        try:
            params = load_YAML_file(args.config);
        except IOError, (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror));
            print("Default configuration file will be used");
        except:
            print("Unexpected error:", sys.exc_info()[0]);
            raise
        
    print("\n ### EXECUTING SOFTWARE TEST ###\n");

    params = None;

    test_passed = fe_test(params, False);

    if(test_passed):
        print("\nSOFTWARE TEST PASSED\n");
        print("\n ### EXECUTING EXPERIMENTS ###\n");
        #fe_experiments(params, False);
    else:
        print("\nSOFTWARE TEST FAILED\n");
