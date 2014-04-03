def faceRecognitionExperiments(showResult):
    '''
    Execute face recognition experiments

    :type showResult: boolean
    :param showResult: show (true) or do not show (false) image with detected faces
    '''

    i = 0;
    peopleNr = 0;
    truePositivesNrDict = {}; # Containing true positives number for each person
    falsePositivesNr = {}; # Containing false positives number for each person

    # Create and populate dictionary with people
    peopleDict = {};

    for videoDir in videoDirectories:

        videoDirCompletePath = framesPath + videoDir;

        for frameFile in listdir(videoDirCompletePath):

            annotationsDict = frames[frameFile];
            faces = annotationsDict[ANNOTATIONS_FACES_KEY];

            for extendedFaceDict in faces:

                faceDict = extendedFaceDict[ANNOTATIONS_FACE_KEY];
                annotatedFaceTag = faceDict[ANNOTATIONS_FACE_TAG_KEY];
                personDict = {};
                personDict[TRUE_POSITIVES_NR_KEY] = 0; ### TO BE CONTINUED ...###
                peopleDict[annotatedFaceTag] = personDict;

    meanDetectionTime = 0;

    framesPath = rootPath + FACE_RECOGNITION_FRAMES_PATH;
    classifierFilesPath = rootPath + CLASSIFIER_FILES_PATH;
    videoDirectories = listdir(framesPath);

    # Build path of file with annotations
    annotationsFile = rootPath + ANNOTATIONS_PATH + 'Annotations.yml';

    # Load annotations
    annotatedData = loadYAMLFile(annotationsFile);

    peopleNr = annotatedData[ANNOTATIONS_PEOPLE_NR_KEY];

    frames = annotatedData[ANNOTATIONS_FRAMES_KEY];

    # Iterate over all directories with test frames
    globalFrameCounter = 0;
    for videoDir in videoDirectories:
        videoDirCompletePath = framesPath + videoDir;

        # Iterate over all frames taken from this video
        frameCounter = 0;
        for frameFile in listdir(videoDirCompletePath):

            annotationsDict = frames[frameFile];

            faces = annotationsDict[ANNOTATIONS_FACES_KEY];

            for extendedFaceDict in faces:

                faceDict = extendedFaceDict[ANNOTATIONS_FACE_KEY];

                annotatedFaceTag = faceDict[ANNOTATIONS_FACE_TAG_KEY];

                x = faceDict[ANNOTATIONS_FACE_X_KEY];
                y = faceDict[ANNOTATIONS_FACE_Y_KEY];
                width = faceDict[ANNOTATIONS_FACE_WIDTH_KEY];
                height = faceDict[ANNOTATIONS_FACE_HEIGHT_KEY];

                # Execute face recognition on given face rectangle
                detectedFaceTag = faceRecognitionFromImage(framePath, [x, y, width, height]);

                # Add recognition time to total
                meanDetectionTime = meanDetectionTime + recognitionResults[FACE_RECOGNITION_ELAPSED_CPU_TIME_KEY];

                # Check correctness of recognition
                if(detectedFaceTag == annotatedFaceTag):
                    detectedFaceInnerDict[FACE_CHECK_KEY] = 'TP'; # Face is a true positive detection
                else:
                    detectedFaceInnerDict[FACE_CHECK_KEY] = 'FP'; # Face is a false positive detection

                # Update results for person with tag annotatedFaceTag

            # Set path of frame and path of directory with classifier files
            framePath = videoDirCompletePath + '\\' + frameFile;


