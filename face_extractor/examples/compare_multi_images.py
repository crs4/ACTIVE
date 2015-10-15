import cv2
import os
import sys

sys.path.append('..')
import tools.constants as c
from tools.face_detection import detect_faces_in_image
from tools.face_models import FaceModels


def main(argv):
	base_name=argv[1]
	for i in range(0,6):
		for j in range(0,5):
			print "**************************************"
			# Set path of images to be analyzed
			image_path_1 = base_name+str(i)+".JPG"

			print "image_path_1 ", image_path_1
			image_path_2 = base_name+str(j)+".JPG"
			print "image_path_2 ", image_path_2

			# Set path of directory where aligned faces will be saved
			align_path = '/tmp'

			# Set parameters
			params = {
			    c.CHECK_EYE_POSITIONS_KEY: True,
			    c.CLASSIFIERS_DIR_PATH_KEY: '/home/active/gitactive/ACTIVE/face_extractor/examples/haarcascades',
			    c.CROPPED_FACE_HEIGHT_KEY: 250,
			    c.CROPPED_FACE_WIDTH_KEY: 200,
			    c.EYE_DETECTION_CLASSIFIER_KEY: 'haarcascade_mcs_lefteye.xml',
			    c.FACE_DETECTION_ALGORITHM_KEY: 'HaarCascadeFrontalFaceAlt2',
			    c.FLAGS_KEY: 'DoCannyPruning',
			    c.MIN_NEIGHBORS_KEY: 5,
			    c.MIN_SIZE_HEIGHT_KEY: 20,
			    c.MIN_SIZE_WIDTH_KEY: 20,
			    c.OFFSET_PCT_X_KEY: 0.30,
			    c.OFFSET_PCT_Y_KEY: 0.42,
			    c.SCALE_FACTOR_KEY: 1.1,
			    c.MAX_EYE_ANGLE_KEY: 0.125,
			    c.MIN_EYE_DISTANCE_KEY: 0.25,
			    c.USE_EYES_POSITION_KEY: True,
			    c.USE_NOSE_POS_IN_DETECTION_KEY: False,
			    c.ALIGNED_FACES_PATH_KEY: align_path,
			    c.GLOBAL_FACE_REC_DATA_DIR_PATH_KEY: '/home/active/gitactive/ACTIVE/face_extractor/examples/face_rec_data2',
			    c.LBP_GRID_X_KEY: 4,
			    c.LBP_GRID_Y_KEY: 5,
			    c.LBP_NEIGHBORS_KEY: 8,
			    c.LBP_RADIUS_KEY: 1
			}

			fm = FaceModels(params)

			# Delete possible already existing models
			fm.delete_models()

			# Add face from first image to face models
			label = 0
			tag = ''
			fm.add_face(label, tag, image_path_1)

			# Detect face in second image
			result = detect_faces_in_image(
			   image_path_2, align_path, params, show_results=False)

			# Recognize aligned face detected in second image
			if result and c.FACES_KEY in result:
			    faces = result[c.FACES_KEY]
			    if len(faces) == 1:

				# Get aligned face and calculate distance between faces
				file_name = faces[0][c.ALIGNED_FACE_FILE_NAME_KEY]
				file_name_complete = file_name + '_gray.png'
				file_path = os.path.join(align_path, file_name_complete)
				aligned_face = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
				(label, conf) = fm.recognize_face(aligned_face)

				# Draw bounding box around face
				img = cv2.imread(image_path_2)
				(x, y, w, h) = faces[0][c.BBOX_KEY]
				cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3, 8, 0)

				# Write distance from reference image
				cv2.putText(img, str(conf), (x, y + h + 30),
					    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				print "distance ", conf
				#cv2.imshow('Image', img)
				#cv2.waitKey(0)

				#image_path_2 = os.path.splitext(image_path_2)[0]
				#image_path_2 = image_path_2 + '_comparison.png'
				#cv2.imwrite(image_path_2, img)

if __name__ == '__main__':
	main(sys.argv)

