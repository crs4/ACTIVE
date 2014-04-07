from face_extractor import  FaceExtractor

resource_path = r'C:\Users\Maurizio\Documents\Progetto ACTIVE\test\Test files\Face detection\TestSet\fic.06\fic.06_I_011.jpg';

fe = FaceExtractor(None);

result = fe.extract_faces_from_image_sync(resource_path);

print(result);
