from face_extractor import  FaceExtractor

resource_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\1.pgm';

fe = FaceExtractor(None);

result = fe.extract_faces_from_image_sync(resource_path);

print(result);
