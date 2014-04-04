from face_extractor import  FaceExtractor

resource_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\TestSet\fic.02\fic.02_I_002.jpg';

fe = FaceExtractor(None);

result = fe.extract_faces_from_image_sync(resource_path);

print(result);
