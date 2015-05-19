import os
import sys
sys.path.append("..")
from tools.Constants import *
from tools.Utils import save_YAML_file

def make_fic02_annotations(file_path):
    '''
    Make annotations for fic.02.mpg video file
    
    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    '''
    
    audio_segments = []
    caption_segments = []
    video_segments = []
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 53
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 42
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 42
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 47
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 49
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 57
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 59
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_END_KEY] = 3*60 + 12
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 3*60 + 27
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_END_KEY] = 3*60 + 35
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 4*60 + 30
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_END_KEY] = 4*60 + 45
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 30
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 40
    video_segments.append(video_segment_dict)
    
    # Tutti e 3 gli ospiti
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 40
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 58
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 40
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_END_KEY] = 7 * 60 + 28
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 40
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 58
    video_segments.append(video_segment_dict)
    
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 54
    audio_segment_dict[SEGMENT_END_KEY] = 6 * 60 + 51
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    caption_segment_dict[SEGMENT_START_KEY] = 63
    caption_segment_dict[SEGMENT_END_KEY] = 67
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 6 * 60 + 40
    audio_segment_dict[SEGMENT_END_KEY] = 7 * 60 + 28
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    caption_segment_dict[SEGMENT_START_KEY] = 7 * 60 + 3
    caption_segment_dict[SEGMENT_END_KEY] =  7 * 60 + 9
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 7 * 60 + 27
    audio_segment_dict[SEGMENT_END_KEY] = 7 * 60 + 33 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 7 * 60 + 33
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    caption_segment_dict[SEGMENT_START_KEY] = 7 * 60 + 37
    caption_segment_dict[SEGMENT_END_KEY] =  7 * 60 + 43
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 7 * 60 + 33
    audio_segment_dict[SEGMENT_END_KEY] = 8 * 60 + 37 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 7 * 60 + 33
    video_segment_dict[SEGMENT_END_KEY] = 7 * 60 + 59
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 8 * 60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 8 * 60 + 38 
    video_segments.append(video_segment_dict)
    
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 8 * 60 + 37
    audio_segment_dict[SEGMENT_END_KEY] = 8 * 60 + 46 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 8 * 60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 8 * 60 + 46
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 8 * 60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 9 * 60 + 5 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 8 * 60 + 46
    video_segment_dict[SEGMENT_END_KEY] = 9 * 60 + 5 
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 9 * 60 + 32
    audio_segment_dict[SEGMENT_END_KEY] = 9 * 60 + 54 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 9 * 60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 9 * 60 + 54
    video_segments.append(video_segment_dict)
    
    # Interviste per strada
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 9 * 60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 9 * 60 + 59 
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 10 * 60 + 12
    audio_segment_dict[SEGMENT_END_KEY] = 10 * 60 + 14
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 10 * 60 + 20
    audio_segment_dict[SEGMENT_END_KEY] = 10 * 60 + 22
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 10 * 60 + 35
    audio_segment_dict[SEGMENT_END_KEY] = 10 * 60 + 39
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 10 * 60 + 45
    audio_segment_dict[SEGMENT_END_KEY] = 10 * 60 + 46
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 10 * 60 + 57
    audio_segment_dict[SEGMENT_END_KEY] = 10 * 60 + 59
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 11 * 60 + 11
    audio_segment_dict[SEGMENT_END_KEY] = 11 * 60 + 12
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 11 * 60 + 31
    audio_segment_dict[SEGMENT_END_KEY] = 11 * 60 + 39
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 11 * 60 + 42
    audio_segment_dict[SEGMENT_END_KEY] = 11 * 60 + 43
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 11 * 60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 11 * 60 + 47
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 12 * 60 + 11
    audio_segment_dict[SEGMENT_END_KEY] = 12 * 60 + 15
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 12 * 60 + 33
    audio_segment_dict[SEGMENT_END_KEY] = 12 * 60 + 35
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 12 * 60 + 50
    audio_segment_dict[SEGMENT_END_KEY] = 12 * 60 + 52
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 13 * 60 + 16
    audio_segment_dict[SEGMENT_END_KEY] = 13 * 60 + 21
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 13 * 60 + 52
    audio_segment_dict[SEGMENT_END_KEY] = 13 * 60 + 56
    audio_segments.append(audio_segment_dict)
    
    # Ritorno in studio
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 17
    audio_segment_dict[SEGMENT_END_KEY] = 14 * 60 + 24 
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 17
    video_segment_dict[SEGMENT_END_KEY] = 14 * 60 + 24
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 24
    audio_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 3
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 14 * 60 + 29
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 14 * 60 + 29
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 4
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    caption_segment_dict[SEGMENT_START_KEY] = 14 * 60 + 34
    caption_segment_dict[SEGMENT_END_KEY] = 14 * 60 + 39
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 5
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 6
    audio_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 27
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 27
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    caption_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 9
    caption_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 14
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 28
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 29
    audio_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 5
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 52
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    caption_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 39
    caption_segment_dict[SEGMENT_END_KEY] = 15 * 60 + 44
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 15 * 60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 7
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 16 * 60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 7
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 16 * 60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 9
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 16 * 60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 7
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 16 * 60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 49
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 16 * 60 + 40
    audio_segment_dict[SEGMENT_END_KEY] = 16 * 60 + 44
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 17
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 11
    audio_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 13
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 13
    audio_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 34
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 17
    video_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 34
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 34
    video_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 38
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 17 * 60 + 34
    audio_segment_dict[SEGMENT_END_KEY] = 17 * 60 + 38
    audio_segments.append(audio_segment_dict)
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 18 * 60
    video_segment_dict[SEGMENT_END_KEY] = 18 * 60 + 25
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 18 * 60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 18 * 60 + 23
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 18 * 60 + 25
    audio_segment_dict[SEGMENT_END_KEY] = 18 * 60 + 54
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 18 * 60 + 25
    video_segment_dict[SEGMENT_END_KEY] = 19 * 60 + 11
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 18 * 60 + 54
    audio_segment_dict[SEGMENT_END_KEY] = 19 * 60 + 29
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    caption_segment_dict[SEGMENT_START_KEY] = 18 * 60 + 56
    caption_segment_dict[SEGMENT_END_KEY] = 18 * 60 + 59
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 19 * 60 + 21
    video_segment_dict[SEGMENT_END_KEY] = 19 * 60 + 31
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 20 * 60 + 4
    audio_segment_dict[SEGMENT_END_KEY] = 20 * 60 + 9
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 19 * 60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 20 * 60 + 36
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 19 * 60 + 32
    audio_segment_dict[SEGMENT_END_KEY] = 20 * 60 + 4
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 20 * 60 + 29
    audio_segment_dict[SEGMENT_END_KEY] = 20 * 60 + 56
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 20 * 60 + 57
    audio_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 4
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    caption_segment_dict[SEGMENT_START_KEY] = 20 * 60 + 10
    caption_segment_dict[SEGMENT_END_KEY] = 20 * 60 + 15
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 20 * 60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 15
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 4
    audio_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 15
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 15
    audio_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 24
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 24
    audio_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 54
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 23 * 60 + 45
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 54
    audio_segment_dict[SEGMENT_END_KEY] = 21 * 60 + 59
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 21 * 60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 22 * 60 + 22
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 22 * 60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 22
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] =24 * 60 + 22
    audio_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 25
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    video_segment_dict[SEGMENT_START_KEY] = 23 * 60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 46
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Caredda_Giorgio'
    audio_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 31
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 55
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 49
    audio_segment_dict[SEGMENT_END_KEY] = 24 * 60 + 55
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 55
    audio_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 43
    audio_segments.append(audio_segment_dict)
    
    # I 3 ospiti in contemporanea
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 1
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 1
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 24 * 60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 45
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    caption_segment_dict[SEGMENT_START_KEY] = 25 * 60 + 7
    caption_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 10
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 25 * 60 + 43
    audio_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 49
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 25 * 60 + 45
    video_segment_dict[SEGMENT_END_KEY] = 25 * 60 + 49
    video_segments.append(video_segment_dict)
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 26 * 60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 26 * 60 +43
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 26 * 60 + 13
    audio_segment_dict[SEGMENT_END_KEY] = 26 * 60 + 41
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    video_segment_dict[SEGMENT_START_KEY] = 26 * 60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 31 * 60 + 35
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 26 * 60 + 43
    audio_segment_dict[SEGMENT_END_KEY] = 27 * 60 + 26
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    caption_segment_dict[SEGMENT_START_KEY] = 26 * 60 + 59
    caption_segment_dict[SEGMENT_END_KEY] = 27 * 60 + 5
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 27 * 60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 27 * 60 + 31
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 27 * 60 + 31
    audio_segment_dict[SEGMENT_END_KEY] = 28 * 60 + 8
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 28 * 60 + 9
    audio_segment_dict[SEGMENT_END_KEY] = 28 * 60 + 20
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 28 * 60 + 21
    audio_segment_dict[SEGMENT_END_KEY] = 29 * 60 + 56
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    caption_segment_dict[SEGMENT_START_KEY] = 28 * 60 + 41
    caption_segment_dict[SEGMENT_END_KEY] = 28 * 60 + 47
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 29 * 60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 30 * 60 + 1
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 30 * 60 + 2
    audio_segment_dict[SEGMENT_END_KEY] = 31 * 60 + 35
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Locatelli_Gianni'
    caption_segment_dict[SEGMENT_START_KEY] = 30 * 60 + 27
    caption_segment_dict[SEGMENT_END_KEY] = 30 * 60 + 31
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 31 * 60 + 37
    video_segment_dict[SEGMENT_END_KEY] = 31 * 60 + 43
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 31 * 60 + 38
    audio_segment_dict[SEGMENT_END_KEY] = 32 * 60 + 4
    audio_segments.append(audio_segment_dict)
    
    # I 3 ospiti in contemporanea
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 31 * 60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 31 * 60 + 57
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 31 * 60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 32 * 60 + 2
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 31 * 60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 32 * 60 + 29
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 32 * 60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 33 * 60 + 46
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    caption_segment_dict[SEGMENT_START_KEY] = 32 * 60 + 21
    caption_segment_dict[SEGMENT_END_KEY] = 32 * 60 + 28
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 32 * 60 + 40
    video_segment_dict[SEGMENT_END_KEY] = 33 * 60 + 4
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 33 * 60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 33 * 60 + 46
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 33 * 60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 33 * 60 + 50
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 33 * 60 + 46
    video_segment_dict[SEGMENT_END_KEY] = 33 * 60 + 53
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 33 * 60 + 51
    audio_segment_dict[SEGMENT_END_KEY] = 34 * 60 + 43
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 33 * 60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 34 * 60 + 30
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    caption_segment_dict[SEGMENT_START_KEY] = 34 * 60 + 14
    caption_segment_dict[SEGMENT_END_KEY] = 34 * 60 + 19
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 34 * 60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 34 * 60 + 56
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 34 * 60 + 43
    audio_segment_dict[SEGMENT_END_KEY] = 34 * 60 + 59
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 34 * 60 + 56
    video_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 6
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 34 * 60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 3
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 24
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 14
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 24
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 27
    audio_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 53
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 53
    audio_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 57
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 57
    audio_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 9
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 9
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    caption_segment_dict[SEGMENT_START_KEY] = 35 * 60 + 38
    caption_segment_dict[SEGMENT_END_KEY] = 35 * 60 + 43
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 9
    audio_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 14
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 14
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 14
    audio_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 37
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 37
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    caption_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 18
    caption_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 22
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 37
    audio_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 45
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 37
    video_segment_dict[SEGMENT_END_KEY] = 36 * 60 + 42
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 50
    audio_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 2
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 37 * 60 + 2
    audio_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 4
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 37 * 60 + 4
    audio_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 34
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 36 * 60 + 52
    video_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 4 
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 37 * 60 + 4
    video_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 8
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 37 * 60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 37
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 37 * 60 + 34
    audio_segment_dict[SEGMENT_END_KEY] = 37 * 60 + 38
    audio_segments.append(audio_segment_dict)
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 20
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 51
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 30
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 30
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 30
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 38 * 60 + 51
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 51
    video_segment_dict[SEGMENT_END_KEY] = 39 * 60 + 10
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 38 * 60 + 51
    audio_segment_dict[SEGMENT_END_KEY] = 40 * 60 + 54
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 39 * 60 + 16
    video_segment_dict[SEGMENT_END_KEY] = 40 * 60 + 25
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 39 * 60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 40 * 60 + 25
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 39 * 60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 40 * 60 + 25 
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 40 * 60 + 25
    video_segment_dict[SEGMENT_END_KEY] =  40 * 60 + 30
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 40 * 60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 40 * 60 + 54
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 40 * 60 + 54
    audio_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 14
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 40 * 60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 3
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 16
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 40
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 3
    video_segment_dict[SEGMENT_END_KEY] =  41 * 60 + 19
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 14
    audio_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 39
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 38
    audio_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 42
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 40
    video_segment_dict[SEGMENT_END_KEY] = 41 * 60 + 47
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 47
    video_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 3
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 41 * 60 + 42
    audio_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 41
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 37
    video_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 50
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 41
    audio_segment_dict[SEGMENT_END_KEY] = 42 * 60 + 45
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 43 * 60 + 2
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 43 * 60 + 46
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 42 * 60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 43 * 60 + 46
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 43 * 60 + 46
    video_segment_dict[SEGMENT_END_KEY] = 43 * 60 + 57
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 43 * 60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 44 * 60 + 5
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 43 * 60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 43 * 60 + 59
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 43 * 60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 44 * 60
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 44 * 60 + 6
    audio_segment_dict[SEGMENT_END_KEY] = 44 * 60 + 19
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 44 * 60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 44 * 60 + 45
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 44 * 60 + 19
    audio_segment_dict[SEGMENT_END_KEY] = 44 * 60 + 22
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 44 * 60 + 21
    audio_segment_dict[SEGMENT_END_KEY] = 45 * 60 + 39
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 45 * 60 + 39
    audio_segment_dict[SEGMENT_END_KEY] = 45 * 60 + 46
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 45 * 60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 47 * 60 + 10
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 47 * 60 + 10
    audio_segment_dict[SEGMENT_END_KEY] = 47 * 60 + 23
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 47 * 60 + 23
    audio_segment_dict[SEGMENT_END_KEY] = 47 * 60 + 36
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 47 * 60 + 36
    audio_segment_dict[SEGMENT_END_KEY] = 47 * 60 + 45
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 47 * 60 + 45
    audio_segment_dict[SEGMENT_END_KEY] = 48 * 60 + 10
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 48 * 60 + 10
    audio_segment_dict[SEGMENT_END_KEY] = 48 * 60 + 12
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Leoni_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 48 * 60 + 12
    audio_segment_dict[SEGMENT_END_KEY] = 49 * 60 + 45
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 48 * 60 + 42
    audio_segment_dict[SEGMENT_END_KEY] = 48 * 60 + 51
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 49 * 60 + 6
    audio_segment_dict[SEGMENT_END_KEY] = 49 * 60 + 8
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 49 * 60 + 45
    audio_segment_dict[SEGMENT_END_KEY] = 49 * 60 + 59
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 50 * 60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 50 * 60 + 16
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    audio_segment_dict[SEGMENT_START_KEY] = 50 * 60 + 14
    audio_segment_dict[SEGMENT_END_KEY] = 51 * 60 + 2
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 50 * 60 + 12
    video_segment_dict[SEGMENT_END_KEY] = 51 * 60 + 3
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    caption_segment_dict[SEGMENT_START_KEY] = 50 * 60 + 19
    caption_segment_dict[SEGMENT_END_KEY] = 50 * 60 + 25
    caption_segments.append(caption_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 51 * 60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 51 * 60 + 20
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 51 * 60 + 4
    video_segment_dict[SEGMENT_END_KEY] = 51 * 60 + 21
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    audio_segment_dict[SEGMENT_START_KEY] = 51 * 60 + 20
    audio_segment_dict[SEGMENT_END_KEY] = 52 * 60 + 44
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    video_segment_dict[SEGMENT_START_KEY] = 51 * 60 + 21
    video_segment_dict[SEGMENT_END_KEY] = 52 * 60 + 44
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Fadda_Paolo'
    caption_segment_dict[SEGMENT_START_KEY] = 51 * 60 + 23
    caption_segment_dict[SEGMENT_END_KEY] = 51 * 60 + 30
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giannotta_Michele'
    video_segment_dict[SEGMENT_START_KEY] = 52 * 60 + 21
    video_segment_dict[SEGMENT_END_KEY] = 52 * 60 + 44
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    audio_segment_dict[SEGMENT_START_KEY] = 52 * 60 + 44
    audio_segment_dict[SEGMENT_END_KEY] = 53 * 60 + 2
    audio_segments.append(audio_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Mameli_Giacomo'
    video_segment_dict[SEGMENT_START_KEY] = 52 * 60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 53 * 60 + 4
    video_segments.append(video_segment_dict)
    
    ann_dict = {}
    
    # Add durations for video segments
       
    new_video_segments = []
    
    tot_segment_duration = 0
       
    for video_segment in video_segments:
        
        new_video_segment =  {}
        ann_tag = video_segment[ANN_TAG_KEY]
        start_time = video_segment[SEGMENT_START_KEY]
        end_time = video_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        
        if(duration < 0):
            
            print('Warning! Negative duration!')
            print('ann_tag', ann_tag)
            print('start_time', start_time)
            print('end_time', end_time)
        
        tot_segment_duration = tot_segment_duration + duration
        new_video_segment[ANN_TAG_KEY] = ann_tag  
        new_video_segment[SEGMENT_START_KEY] = start_time
        new_video_segment[SEGMENT_DURATION_KEY] = duration
        # transform seconds in milliseconds
        new_video_segment[SEGMENT_START_KEY] = start_time * 1000
        new_video_segment[SEGMENT_DURATION_KEY] = duration * 1000
        new_video_segments.append(new_video_segment)
    
    ann_dict[VIDEO_SEGMENTS_KEY] = new_video_segments
    
    ann_dict[TOT_SEGMENT_DURATION_KEY] = tot_segment_duration
    
    # Add durations for audio and caption segments
    
    for i in range(0, len(audio_segments)):
        audio_segment = audio_segments[i]
        start_time = audio_segment[SEGMENT_START_KEY]
        end_time = audio_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        audio_segments[i][SEGMENT_DURATION_KEY] = duration
        
    for i in range(0, len(caption_segments)):
        caption_segment = caption_segments[i]
        start_time = caption_segment[SEGMENT_START_KEY]
        end_time = caption_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        caption_segments[i][SEGMENT_DURATION_KEY] = duration
        
    ann_dict[AUDIO_SEGMENTS_KEY] = audio_segments
    ann_dict[CAPTION_SEGMENTS_KEY] = caption_segments
    
    save_YAML_file(file_path, ann_dict)
    
    return ann_dict
    
    
def make_MONITOR072011_annotations(file_path):
    '''
    Make annotations for MONITOR072011.mpg video file
    
    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    '''
    
    audio_segments = []
    caption_segments = []
    video_segments = []
    '''
    Templates
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = ''
    video_segment_dict[SEGMENT_START_KEY] = 
    video_segment_dict[SEGMENT_END_KEY] = 
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = ''
    audio_segment_dict[SEGMENT_START_KEY] = 
    audio_segment_dict[SEGMENT_END_KEY] = 
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = ''
    caption_segment_dict[SEGMENT_START_KEY] = 
    caption_segment_dict[SEGMENT_END_KEY] =  
    caption_segments.append(caption_segment_dict)
    '''
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 32
    video_segment_dict[SEGMENT_END_KEY] = 41
    video_segments.append(video_segment_dict)    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 48
    video_segment_dict[SEGMENT_END_KEY] = 52
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3*60 + 35
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 6
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    caption_segment_dict[SEGMENT_START_KEY] = 4*60 + 56
    caption_segment_dict[SEGMENT_END_KEY] = 5*60 + 4
    caption_segments.append(caption_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 35
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 44
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 5
    video_segments.append(video_segment_dict)   
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    caption_segment_dict[SEGMENT_START_KEY] = 6*60 + 15
    caption_segment_dict[SEGMENT_END_KEY] =  6*60 + 24
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 5
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 5
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 5
    video_segments.append(video_segment_dict)
    
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 5
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 32
    video_segments.append(video_segment_dict)
    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 7*60+49
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 38
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 43
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 8*60+47
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 40
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 7*60+49
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 7*60+49
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 40
    video_segment_dict[SEGMENT_END_KEY] = 7*60+49
    video_segments.append(video_segment_dict)   
    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 9*60+22
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 9*60+11
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 9*60+10
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 9*60 + 24
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 9*60 + 27
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 9*60 + 30
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 9*60+40
    video_segment_dict[SEGMENT_END_KEY] = 9*60+57
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+4
    video_segment_dict[SEGMENT_END_KEY] = 10*60+27
    video_segments.append(video_segment_dict)  
    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+13
    video_segment_dict[SEGMENT_END_KEY] = 10*60+22
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+13
    video_segment_dict[SEGMENT_END_KEY] = 10*60+22
    video_segments.append(video_segment_dict)
    
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+13
    video_segment_dict[SEGMENT_END_KEY] = 10*60+22
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+27
    video_segment_dict[SEGMENT_END_KEY] = 10*60+34
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 10*60+39
    video_segment_dict[SEGMENT_END_KEY] = 11*60
    video_segments.append(video_segment_dict)           
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+4
    video_segment_dict[SEGMENT_END_KEY] = 11*60+16
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+4
    video_segment_dict[SEGMENT_END_KEY] = 11*60+16
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+4
    video_segment_dict[SEGMENT_END_KEY] = 11*60+16
    video_segments.append(video_segment_dict)    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+16
    video_segment_dict[SEGMENT_END_KEY] = 11*60+20
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+20
    video_segment_dict[SEGMENT_END_KEY] = 11*60+24
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+20
    video_segment_dict[SEGMENT_END_KEY] = 11*60+24
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 11*60+20
    video_segment_dict[SEGMENT_END_KEY] = 11*60+24
    video_segments.append(video_segment_dict)
    
    
    # 5 people at the same time
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 11*60+32
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 11*60+32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 11*60+32
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 11*60 + 32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 11*60+58
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 12*60+1
    video_segment_dict[SEGMENT_END_KEY] = 12*60+5
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 12*60+10
    video_segment_dict[SEGMENT_END_KEY] = 12*60+16
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 12*60+16
    video_segment_dict[SEGMENT_END_KEY] = 13*60+8
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 13*60+12
    video_segment_dict[SEGMENT_END_KEY] = 13*60+21
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 13*60+25
    video_segment_dict[SEGMENT_END_KEY] = 13*60+55
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 13*60+36
    video_segment_dict[SEGMENT_END_KEY] = 13*60+55
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 13*60+36
    video_segment_dict[SEGMENT_END_KEY] = 13*60+55
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 13*60+55
    video_segment_dict[SEGMENT_END_KEY] = 14*60+8
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 14*60+14
    video_segment_dict[SEGMENT_END_KEY] = 14*60+19
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 14*60+26
    video_segment_dict[SEGMENT_END_KEY] = 14*60+41
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    caption_segment_dict[SEGMENT_START_KEY] = 14*60+35
    caption_segment_dict[SEGMENT_END_KEY] = 14*60+43
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 14*60+42
    video_segment_dict[SEGMENT_END_KEY] = 14*60+50
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 14*60+50
    video_segment_dict[SEGMENT_END_KEY] = 14*60+53
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 14*60+53
    video_segment_dict[SEGMENT_END_KEY] = 15*60+6
    video_segments.append(video_segment_dict)
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 18*60+53
    video_segment_dict[SEGMENT_END_KEY] = 19*60+43
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 19*60+48
    video_segment_dict[SEGMENT_END_KEY] = 19*60+55
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 19*60+55
    video_segment_dict[SEGMENT_END_KEY] = 19*60+57
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 19*60+57
    video_segment_dict[SEGMENT_END_KEY] = 21*60+4
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    caption_segment_dict[SEGMENT_START_KEY] = 20*60+4
    caption_segment_dict[SEGMENT_END_KEY] = 20*60+20
    caption_segments.append(caption_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+9
    video_segment_dict[SEGMENT_END_KEY] = 21*60+23
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+23
    video_segment_dict[SEGMENT_END_KEY] = 21*60+29
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+31
    video_segment_dict[SEGMENT_END_KEY] = 21*60+36
    video_segments.append(video_segment_dict)   
    
    # 3 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+36
    video_segment_dict[SEGMENT_END_KEY] = 21*60+38
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+36
    video_segment_dict[SEGMENT_END_KEY] = 21*60+38
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+36
    video_segment_dict[SEGMENT_END_KEY] = 21*60+38
    video_segments.append(video_segment_dict)  
    
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 21*60+38
    video_segment_dict[SEGMENT_END_KEY] = 22*60+6
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+6 
    video_segment_dict[SEGMENT_END_KEY] = 22*60+9
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+9
    video_segment_dict[SEGMENT_END_KEY] = 22*60+33
    video_segments.append(video_segment_dict)  
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    caption_segment_dict[SEGMENT_START_KEY] = 22*60+16
    caption_segment_dict[SEGMENT_END_KEY] = 22*60+30
    caption_segments.append(caption_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+33
    video_segment_dict[SEGMENT_END_KEY] = 22*60+43
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+41
    video_segment_dict[SEGMENT_END_KEY] = 22*60+43
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+41
    video_segment_dict[SEGMENT_END_KEY] = 22*60+43
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 22*60+43
    video_segment_dict[SEGMENT_END_KEY] = 23*60+7
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 23*60+17
    video_segment_dict[SEGMENT_END_KEY] = 23*60+21
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 23*60+24
    video_segment_dict[SEGMENT_END_KEY] = 24*60+1
    video_segments.append(video_segment_dict)   

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 24*60+18
    video_segment_dict[SEGMENT_END_KEY] = 24*60+21
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 24*60+21
    video_segment_dict[SEGMENT_END_KEY] = 24*60+37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 24*60+48
    video_segment_dict[SEGMENT_END_KEY] = 25*60+7
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 25*60+27
    video_segment_dict[SEGMENT_END_KEY] = 25*60+33
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 25*60+33
    video_segment_dict[SEGMENT_END_KEY] = 25*60+47
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 25*60+51
    video_segment_dict[SEGMENT_END_KEY] = 25*60+58
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 26*60+2
    video_segment_dict[SEGMENT_END_KEY] = 26*60+8
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 26*60+18
    video_segment_dict[SEGMENT_END_KEY] = 26*60+26
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 26*60+26
    video_segment_dict[SEGMENT_END_KEY] = 26*60+31
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 26*60+31
    video_segment_dict[SEGMENT_END_KEY] = 27*60+20
    video_segments.append(video_segment_dict)  
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    caption_segment_dict[SEGMENT_START_KEY] = 26*60+44
    caption_segment_dict[SEGMENT_END_KEY] = 26*60+54
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 27*60+35
    video_segment_dict[SEGMENT_END_KEY] = 28*60+12
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+6
    video_segment_dict[SEGMENT_END_KEY] = 28*60+12
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+6
    video_segment_dict[SEGMENT_END_KEY] = 28*60+12
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+6
    video_segment_dict[SEGMENT_END_KEY] = 28*60+12
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+6
    video_segment_dict[SEGMENT_END_KEY] = 28*60+12
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+21
    video_segment_dict[SEGMENT_END_KEY] = 28*60+26
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+21
    video_segment_dict[SEGMENT_END_KEY] = 28*60+26
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+21
    video_segment_dict[SEGMENT_END_KEY] = 29*60+6
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+21
    video_segment_dict[SEGMENT_END_KEY] = 28*60+26
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 28*60+21
    video_segment_dict[SEGMENT_END_KEY] = 28*60+26
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    caption_segment_dict[SEGMENT_START_KEY] = 28*60+34
    caption_segment_dict[SEGMENT_END_KEY] = 28*60+40
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 29*60+25
    video_segment_dict[SEGMENT_END_KEY] = 29*60+41
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 29*60+55
    video_segment_dict[SEGMENT_END_KEY] = 29*60+59
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 30*60+7
    video_segment_dict[SEGMENT_END_KEY] = 30*60+30
    video_segments.append(video_segment_dict)      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 30*60+30
    video_segment_dict[SEGMENT_END_KEY] = 30*60+37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 30*60+41
    video_segment_dict[SEGMENT_END_KEY] = 31*60+46
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 31*60+50
    video_segment_dict[SEGMENT_END_KEY] = 32*60 + 7
    video_segments.append(video_segment_dict) 
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 35*60+38
    video_segment_dict[SEGMENT_END_KEY] = 35*60+49
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 35*60+55
    video_segment_dict[SEGMENT_END_KEY] = 35*60+56
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 36*60
    video_segment_dict[SEGMENT_END_KEY] = 36*60+6
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    caption_segment_dict[SEGMENT_START_KEY] = 36*60+18
    caption_segment_dict[SEGMENT_END_KEY] = 40*60+10
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 36*60+23
    video_segment_dict[SEGMENT_END_KEY] = 36*60+50
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 36*60+59
    video_segment_dict[SEGMENT_END_KEY] = 37*60+4
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 37*60+4
    video_segment_dict[SEGMENT_END_KEY] = 37*60+15
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 37*60+38
    video_segment_dict[SEGMENT_END_KEY] = 37*60+44
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 37*60+44
    video_segment_dict[SEGMENT_END_KEY] = 37*60+50
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 37*60+59
    video_segment_dict[SEGMENT_END_KEY] = 38*60+2
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+2
    video_segment_dict[SEGMENT_END_KEY] = 38*60+19
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+19
    video_segment_dict[SEGMENT_END_KEY] = 38*60+23
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+19
    video_segment_dict[SEGMENT_END_KEY] = 38*60+29 
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+23
    video_segment_dict[SEGMENT_END_KEY] = 38*60+32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+25
    video_segment_dict[SEGMENT_END_KEY] = 38*60+33
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+28
    video_segment_dict[SEGMENT_END_KEY] = 38*60+37
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+30
    video_segment_dict[SEGMENT_END_KEY] = 38*60+37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+33
    video_segment_dict[SEGMENT_END_KEY] = 38*60+37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+37
    video_segment_dict[SEGMENT_END_KEY] = 38*60+48
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+48
    video_segment_dict[SEGMENT_END_KEY] = 38*60+55
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 38*60+55
    video_segment_dict[SEGMENT_END_KEY] = 39*60+2
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 39*60+21
    video_segment_dict[SEGMENT_END_KEY] = 40*60+23
    video_segments.append(video_segment_dict)
    
    # 4 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 40*60+23
    video_segment_dict[SEGMENT_END_KEY] = 40*60+32
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 40*60+23
    video_segment_dict[SEGMENT_END_KEY] = 40*60+32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 40*60+23
    video_segment_dict[SEGMENT_END_KEY] = 40*60+32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 40*60+23
    video_segment_dict[SEGMENT_END_KEY] = 40*60+32
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 40*60+43
    video_segment_dict[SEGMENT_END_KEY] = 41*60+35
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    caption_segment_dict[SEGMENT_START_KEY] = 40*60+56
    caption_segment_dict[SEGMENT_END_KEY] = 41*60+6
    caption_segments.append(caption_segment_dict)   
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+16
    video_segment_dict[SEGMENT_END_KEY] = 41*60+23
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+16
    video_segment_dict[SEGMENT_END_KEY] = 41*60+23
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+16
    video_segment_dict[SEGMENT_END_KEY] = 41*60+23
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+16
    video_segment_dict[SEGMENT_END_KEY] = 41*60+23
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+43
    video_segment_dict[SEGMENT_END_KEY] = 42*60
    video_segments.append(video_segment_dict)
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+54
    video_segment_dict[SEGMENT_END_KEY] = 42*60
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+54
    video_segment_dict[SEGMENT_END_KEY] = 42*60
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+54
    video_segment_dict[SEGMENT_END_KEY] = 42*60
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 41*60+54
    video_segment_dict[SEGMENT_END_KEY] = 42*60
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 42*60
    video_segment_dict[SEGMENT_END_KEY] = 42*60+8
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+8
    video_segment_dict[SEGMENT_END_KEY] = 42*60+38
    video_segments.append(video_segment_dict)
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+31
    video_segment_dict[SEGMENT_END_KEY] = 42*60+38
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+31
    video_segment_dict[SEGMENT_END_KEY] = 42*60+38
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+31
    video_segment_dict[SEGMENT_END_KEY] = 42*60+38
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+31
    video_segment_dict[SEGMENT_END_KEY] = 42*60+38
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 42*60+53
    video_segment_dict[SEGMENT_END_KEY] = 43*60+4
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+4
    video_segment_dict[SEGMENT_END_KEY] = 43*60+6
    video_segments.append(video_segment_dict) 
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+6
    video_segment_dict[SEGMENT_END_KEY] = 43*60+9
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+6
    video_segment_dict[SEGMENT_END_KEY] = 43*60+15
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+6
    video_segment_dict[SEGMENT_END_KEY] = 43*60+9
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+6
    video_segment_dict[SEGMENT_END_KEY] = 43*60+9
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+6
    video_segment_dict[SEGMENT_END_KEY] = 43*60+9
    video_segments.append(video_segment_dict)  
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+11
    video_segment_dict[SEGMENT_END_KEY] = 43*60+15
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+11
    video_segment_dict[SEGMENT_END_KEY] = 43*60+15
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+11
    video_segment_dict[SEGMENT_END_KEY] = 43*60+15
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+11
    video_segment_dict[SEGMENT_END_KEY] = 43*60+15
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+15
    video_segment_dict[SEGMENT_END_KEY] = 43*60+18
    video_segments.append(video_segment_dict)     
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+18
    video_segment_dict[SEGMENT_END_KEY] = 44*60+6
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    caption_segment_dict[SEGMENT_START_KEY] = 43*60+31
    caption_segment_dict[SEGMENT_END_KEY] = 43*60+41
    caption_segments.append(caption_segment_dict)
 
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+44
    video_segment_dict[SEGMENT_END_KEY] = 44*60
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+44
    video_segment_dict[SEGMENT_END_KEY] = 44*60
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+44
    video_segment_dict[SEGMENT_END_KEY] = 44*60
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 43*60+44
    video_segment_dict[SEGMENT_END_KEY] = 44*60
    video_segments.append(video_segment_dict)                   
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+6
    video_segment_dict[SEGMENT_END_KEY] = 44*60+13
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+13
    video_segment_dict[SEGMENT_END_KEY] = 44*60+21
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+21
    video_segment_dict[SEGMENT_END_KEY] = 44*60+25
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+25
    video_segment_dict[SEGMENT_END_KEY] = 44*60+37
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+37
    video_segment_dict[SEGMENT_END_KEY] = 44*60+44
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 44*60+53
    video_segment_dict[SEGMENT_END_KEY] = 45*60+9
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 45*60+14
    video_segment_dict[SEGMENT_END_KEY] = 45*60+40 
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 45*60+44
    video_segment_dict[SEGMENT_END_KEY] = 46*60+8
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    caption_segment_dict[SEGMENT_START_KEY] = 46*60+4
    caption_segment_dict[SEGMENT_END_KEY] = 46*60+7
    caption_segments.append(caption_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+9
    video_segment_dict[SEGMENT_END_KEY] = 46*60+13
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+14
    video_segment_dict[SEGMENT_END_KEY] = 46*60+26
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+31
    video_segment_dict[SEGMENT_END_KEY] = 46*60+41
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+41
    video_segment_dict[SEGMENT_END_KEY] = 46*60+46
    video_segments.append(video_segment_dict)                     
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+41
    video_segment_dict[SEGMENT_END_KEY] = 46*60+44
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+45
    video_segment_dict[SEGMENT_END_KEY] = 46*60+52
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+48
    video_segment_dict[SEGMENT_END_KEY] = 46*60+52
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+52
    video_segment_dict[SEGMENT_END_KEY] = 46*60+56
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 46*60+56
    video_segment_dict[SEGMENT_END_KEY] = 47*60+2
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 47*60+3
    video_segment_dict[SEGMENT_END_KEY] = 47*60+5
    video_segments.append(video_segment_dict) 
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+33
    video_segment_dict[SEGMENT_END_KEY] = 50*60+55
    video_segments.append(video_segment_dict)
    
    # 5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+55
    video_segment_dict[SEGMENT_END_KEY] =  50*60+58
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+55
    video_segment_dict[SEGMENT_END_KEY] = 51*60+5
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+55
    video_segment_dict[SEGMENT_END_KEY] = 51*60+6
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+55
    video_segment_dict[SEGMENT_END_KEY] = 51*60
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+55
    video_segment_dict[SEGMENT_END_KEY] = 51*60+2
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+58
    video_segment_dict[SEGMENT_END_KEY] = 51*60+6
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 50*60+59
    video_segment_dict[SEGMENT_END_KEY] = 51*60+6
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 51*60+2
    video_segment_dict[SEGMENT_END_KEY] = 52*60+2
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    caption_segment_dict[SEGMENT_START_KEY] = 51*60+26
    caption_segment_dict[SEGMENT_END_KEY] = 51*60+31
    caption_segments.append(caption_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+3
    video_segment_dict[SEGMENT_END_KEY] = 52*60+8
    video_segments.append(video_segment_dict)         

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+8
    video_segment_dict[SEGMENT_END_KEY] = 52*60+13
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+18
    video_segment_dict[SEGMENT_END_KEY] = 52*60+24
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+28
    video_segment_dict[SEGMENT_END_KEY] = 52*60+50
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    caption_segment_dict[SEGMENT_START_KEY] = 52*60+33
    caption_segment_dict[SEGMENT_END_KEY] = 52*60+50
    caption_segments.append(caption_segment_dict)  
    
    #3 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+50
    video_segment_dict[SEGMENT_END_KEY] = 53*60+5
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+50
    video_segment_dict[SEGMENT_END_KEY] = 53*60
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 52*60+50
    video_segment_dict[SEGMENT_END_KEY] = 53*60
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+5
    video_segment_dict[SEGMENT_END_KEY] = 53*60+15
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+15
    video_segment_dict[SEGMENT_END_KEY] = 53*60+21
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+21
    video_segment_dict[SEGMENT_END_KEY] = 53*60+29
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+29
    video_segment_dict[SEGMENT_END_KEY] = 53*60+37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+29
    video_segment_dict[SEGMENT_END_KEY] = 53*60+35
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+29
    video_segment_dict[SEGMENT_END_KEY] = 53*60+34
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+35
    video_segment_dict[SEGMENT_END_KEY] = 53*60+45
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+37
    video_segment_dict[SEGMENT_END_KEY] = 53*60+45
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+45
    video_segment_dict[SEGMENT_END_KEY] = 53*60+53
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+53
    video_segment_dict[SEGMENT_END_KEY] = 53*60+58
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 53*60+58
    video_segment_dict[SEGMENT_END_KEY] = 54*60+14
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 54*60+14
    video_segment_dict[SEGMENT_END_KEY] = 54*60+20
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 54*60+28
    video_segment_dict[SEGMENT_END_KEY] = 54*60+32
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 54*60+37
    video_segment_dict[SEGMENT_END_KEY] = 54*60+59
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 55*60+11
    video_segment_dict[SEGMENT_END_KEY] = 55*60+22
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 55*60+22
    video_segment_dict[SEGMENT_END_KEY] = 55*60+30
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 55*60+46
    video_segment_dict[SEGMENT_END_KEY] = 55*60+49
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 55*60+49
    video_segment_dict[SEGMENT_END_KEY] = 56*60+2
    video_segments.append(video_segment_dict)      

    #3 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+2
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+2
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+2
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+6
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+8
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+9
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+10
    video_segment_dict[SEGMENT_END_KEY] = 56*60+11
    video_segments.append(video_segment_dict)   
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+11
    video_segment_dict[SEGMENT_END_KEY] = 56*60+14
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+14
    video_segment_dict[SEGMENT_END_KEY] = 56*60+33
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 56*60+39
    video_segment_dict[SEGMENT_END_KEY] = 57*60+17
    video_segments.append(video_segment_dict)  
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    caption_segment_dict[SEGMENT_START_KEY] = 56*60+46
    caption_segment_dict[SEGMENT_END_KEY] = 56*60+54 
    caption_segments.append(caption_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 57*60+21
    video_segment_dict[SEGMENT_END_KEY] = 57*60+25
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 57*60+25
    video_segment_dict[SEGMENT_END_KEY] = 57*60+29
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 57*60+42
    video_segment_dict[SEGMENT_END_KEY] = 57*60+57
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 57*60+57
    video_segment_dict[SEGMENT_END_KEY] = 58*60+7
    video_segments.append(video_segment_dict)          

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 58*60+15
    video_segment_dict[SEGMENT_END_KEY] = 1*3600 + 4
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    caption_segment_dict[SEGMENT_START_KEY] = 58*60+27
    caption_segment_dict[SEGMENT_END_KEY] = 58*60+35 
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 1*3600 + 10
    video_segment_dict[SEGMENT_END_KEY] = 1*3600 + 39
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 1*3600 + 39
    video_segment_dict[SEGMENT_END_KEY] = 1*3600 + 42
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 1*3600 + 43
    video_segment_dict[SEGMENT_END_KEY] = 1*3600 + 59
    video_segments.append(video_segment_dict)              

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 59
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 5
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 59
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 8
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 14
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 14
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 60 + 7
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 45
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 60 + 14
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 21
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 26
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 26
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 31
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 31
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 44
    video_segments.append(video_segment_dict)      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 44 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 49
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 51
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 51 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 57
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 3*60 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 3*60 + 5
    video_segments.append(video_segment_dict) 
    
    # Pubblicita'
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 5*60 + 32
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 14
    video_segments.append(video_segment_dict)      
 
    #5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 14
    video_segments.append(video_segment_dict)

    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 14
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 14
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 14
    video_segments.append(video_segment_dict)  

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 53
    caption_segment_dict[SEGMENT_END_KEY] =  3600 + 8*60 + 50
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 22
    video_segments.append(video_segment_dict)  
    
    #5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 27
    video_segments.append(video_segment_dict)      
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 27
    video_segments.append(video_segment_dict)

    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 27
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 27
    video_segments.append(video_segment_dict)      
       
     #5 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)      
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)

    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)        

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 23
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 28
    video_segments.append(video_segment_dict)            
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 39
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 51
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 14
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 19
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 48
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 50
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 53
    caption_segment_dict[SEGMENT_END_KEY] = 3600 + 9*60 + 16
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 9*60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 9*60 + 42
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 9*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 9*60 + 59
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 10*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 10*60 + 12
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 10*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 10*60 + 42
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 10*60 + 57
    caption_segment_dict[SEGMENT_END_KEY] = 3600 + 12*60 + 7
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 11*60 + 15
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 11*60 + 20
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 11*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 12*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 12*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 13
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 12*60 + 40
    caption_segment_dict[SEGMENT_END_KEY] = 3600 + 12*60 + 50
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 16
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 16
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 31
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 43
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 47
    video_segments.append(video_segment_dict)      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 50
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 45
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 55
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 46
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 55
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 48
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 55
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 51
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 13*60 + 55
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 13*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 14*60 + 5
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 14*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 14*60 + 24
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 14*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 14*60 + 49
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 14*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 15*60 + 6 
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 41
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 53
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 57
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 19*60 + 43
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 19*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 19*60 + 46
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 19*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 20*60 + 22
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 20*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 3
    video_segments.append(video_segment_dict) 

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'De_Berardinis_Gianni'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 20*60 + 45
    caption_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 8 
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 21
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 35
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 35 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 44
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 35 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 44
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 35  
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 44
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 40  
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 44
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 21*60 + 55
    video_segments.append(video_segment_dict)              

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 21*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 7
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 7
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 14
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 7 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 14
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 33
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 12 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 30
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 15
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 33
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 57
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 7
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 7
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 13
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 13 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 19
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 25
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 25
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 43
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 24*60 + 32
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 24*60 + 11
    caption_segment_dict[SEGMENT_END_KEY] =  3600 + 24*60 + 24
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 24*60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 25*60 + 13
    video_segments.append(video_segment_dict) 

    # 4 persone contemporaneamente
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 13 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 25*60 + 19
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 25*60 + 20
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 25*60 + 20
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60
    video_segments.append(video_segment_dict)   

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 25
    caption_segment_dict[SEGMENT_END_KEY] =  3600 + 25*60 + 35
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 4
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 11
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 46
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60 + 46
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 48
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 26*60 + 48
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 59
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 37
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 29
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 14
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 14
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 37
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 42
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 45
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 28*60 + 29
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 36
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 28*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 43
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 28*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 47
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 28*60 + 47
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 49
    video_segments.append(video_segment_dict) 
    
    # Pubblicita'

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 32*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 5
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 50
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 11
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 19
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 24
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 46
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 46
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 38
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 46
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 33*60 + 53
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 33*60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 34*60 + 49
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 34*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 34*60 + 7
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 34*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 34*60 + 7
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 34*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 34*60 + 19
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 34*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 34*60 + 19
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 34*60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 18
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 12
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 5
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 12
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 24
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 44
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 30
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 55
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] =  3600 + 35*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 55
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 35*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 55
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] =  3600 + 35*60 + 50
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 35*60 + 55
    video_segments.append(video_segment_dict)
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 29
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 33
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 46
    video_segments.append(video_segment_dict)
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 52
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 52
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 36*60 + 55
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 36*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 22
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 18
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 18
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 18
    video_segments.append(video_segment_dict) 
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 18
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 18
    video_segments.append(video_segment_dict) 

    # 6 persone contemporaneamente

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 30
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 57
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 30
    video_segments.append(video_segment_dict) 
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 30
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 38*60 + 30
    video_segments.append(video_segment_dict)   

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 38*60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 39*60
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 39*60
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 39*60 + 22
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 39*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 39*60 + 26
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 39*60 + 26
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 39*60 + 44
    video_segments.append(video_segment_dict) 
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 39*60 + 44
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 40*60 + 13
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 40*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 40*60 + 20
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 40*60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 40*60 + 43
    video_segments.append(video_segment_dict)  

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Dessalvi_Annalisa'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 40*60 + 36
    caption_segment_dict[SEGMENT_END_KEY] =  3600 + 43*60 + 18
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 40*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 40*60 + 48
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 40*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 41*60 + 6
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 41*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 41*60 + 32
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 41*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 41*60 + 44
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 41*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 42*60 + 12
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 42*60 + 17
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 42*60 + 23
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 42*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 42*60 + 36
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 42*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 42*60 + 42
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 42*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 42*60 + 49
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 42*60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 8
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 13
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 25
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 25 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 27
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 31
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 31
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 42
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 24
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 45
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 45
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 45
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 45
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 43*60 + 45
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 12
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 13
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 43*60 + 58
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 13
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 44*60 + 24 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 29
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 44*60 + 29
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 44*60 + 47
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 44*60 + 47 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 45*60
    video_segments.append(video_segment_dict)
    
    # Pubblicita'

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 48*60 + 30 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 48*60 + 37
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 48*60 + 37
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 48*60 + 43
    video_segments.append(video_segment_dict)   

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 48*60 + 43 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 48*60 + 52
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 48*60 + 52
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 49*60 + 3 
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 49*60 + 3  
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 49*60 + 5
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 49*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 49*60 + 24
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    caption_segment_dict[SEGMENT_START_KEY] = 3600 + 49*60 + 16
    caption_segment_dict[SEGMENT_END_KEY] = 3600 + 49*60 + 23
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 49*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 50*60 + 5
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 50*60 + 13  
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 50*60 + 19
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 50*60 + 19
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 50*60 + 41
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 50*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 1
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 50*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 1
    video_segments.append(video_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 51*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 10
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 51*60 + 10 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 19
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 51*60 + 19
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 51*60 + 30 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 35
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 51*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 51*60 + 57
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 1 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 4
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 4
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 6
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 23
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 32
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 32
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 36
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 52*60 + 40
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 52*60 + 40
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 53*60 + 43
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 53*60 + 43
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 53*60 + 50
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 53*60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 54*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 54*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 54*60 + 44
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 54*60 + 49 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 55*60 + 6
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 55*60 + 12 
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 55*60 + 24
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 55*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 55*60 + 40
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 55*60 + 40
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 16
    video_segments.append(video_segment_dict)
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 33
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 34
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 38
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 34
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 38
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 34
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 38
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 34
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 21
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 57
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 57
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 56*60 + 53
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 56*60 + 57
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 16
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 21
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 24
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 30
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 30
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 35
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 2
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 57*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 57*60 + 47
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 58*60
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 2
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 58*60
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 2
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 58*60
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 2
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 58*60 + 2
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 7
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 58*60 + 9
    video_segment_dict[SEGMENT_END_KEY] = 3600 + 58*60 + 37
    video_segments.append(video_segment_dict) 

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3*60 + 6
    audio_segment_dict[SEGMENT_END_KEY] = 3*60 + 41
    audio_segments.append(audio_segment_dict)   

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    audio_segment_dict[SEGMENT_START_KEY] = 3*60 + 43
    audio_segment_dict[SEGMENT_END_KEY] =  5*60 + 37
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 5*60 + 38
    audio_segment_dict[SEGMENT_END_KEY] = 5*60 + 55
    audio_segments.append(audio_segment_dict)   

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 5*60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 7*60 + 3
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 7*60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 7*60 + 45
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 7*60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 8*60 + 26
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 8*60 + 27
    audio_segment_dict[SEGMENT_END_KEY] = 8*60 + 33
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 8*60 + 34
    audio_segment_dict[SEGMENT_END_KEY] = 9*60 + 20
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 9*60 + 20
    audio_segment_dict[SEGMENT_END_KEY] = 9*60 + 23
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 9*60 + 23
    audio_segment_dict[SEGMENT_END_KEY] = 9*60 + 26
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 9*60 + 29
    audio_segment_dict[SEGMENT_END_KEY] = 10*60 + 24
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 10*60 + 27
    audio_segment_dict[SEGMENT_END_KEY] = 10*60 + 39
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    audio_segment_dict[SEGMENT_START_KEY] = 10*60 + 39
    audio_segment_dict[SEGMENT_END_KEY] = 10*60 + 59
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 10*60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 11*60 + 14
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 11*60 + 14
    audio_segment_dict[SEGMENT_END_KEY] = 11*60 + 19
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 11*60 + 19
    audio_segment_dict[SEGMENT_END_KEY] = 11*60 + 23
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    audio_segment_dict[SEGMENT_START_KEY] = 11*60 + 25
    audio_segment_dict[SEGMENT_END_KEY] = 12*60 + 8
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 12*60 + 8
    audio_segment_dict[SEGMENT_END_KEY] = 12*60 + 16
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    audio_segment_dict[SEGMENT_START_KEY] = 12*60 + 17
    audio_segment_dict[SEGMENT_END_KEY] = 13*60 + 5
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 13*60 + 6
    audio_segment_dict[SEGMENT_END_KEY] = 13*60 + 19
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 13*60 + 19
    audio_segment_dict[SEGMENT_END_KEY] = 13*60 + 22
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    audio_segment_dict[SEGMENT_START_KEY] = 13*60 + 22
    audio_segment_dict[SEGMENT_END_KEY] = 13*60 + 48
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 13*60 + 49
    audio_segment_dict[SEGMENT_END_KEY] = 14*60 + 18
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 14*60 + 18
    audio_segment_dict[SEGMENT_END_KEY] = 14*60 + 39
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 14*60 + 40
    audio_segment_dict[SEGMENT_END_KEY] = 15*60 + 6
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 18*60 + 51
    audio_segment_dict[SEGMENT_END_KEY] = 19*60 + 55
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    audio_segment_dict[SEGMENT_START_KEY] = 19*60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 21*60 + 18
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 21*60 + 20
    audio_segment_dict[SEGMENT_END_KEY] = 21*60 + 28
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    audio_segment_dict[SEGMENT_START_KEY] = 21*60 + 28
    audio_segment_dict[SEGMENT_END_KEY] = 23*60 +  10
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 23*60 + 11
    audio_segment_dict[SEGMENT_END_KEY] = 23*60 + 19
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    audio_segment_dict[SEGMENT_START_KEY] = 23*60 + 20
    audio_segment_dict[SEGMENT_END_KEY] = 25*60 + 58  
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 25*60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 26*60 + 31
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 26*60 + 31
    audio_segment_dict[SEGMENT_END_KEY] = 28*60 + 10 
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 28*60 + 11
    audio_segment_dict[SEGMENT_END_KEY] = 28*60 + 15
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 28*60 + 16
    audio_segment_dict[SEGMENT_END_KEY] = 30*60 + 27 
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 30*60 + 28
    audio_segment_dict[SEGMENT_END_KEY] = 30*60 + 36
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 30*60 + 36
    audio_segment_dict[SEGMENT_END_KEY] = 31*60 + 48
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 31*60 + 48
    audio_segment_dict[SEGMENT_END_KEY] = 32*60 + 7 
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 35*60 + 36
    audio_segment_dict[SEGMENT_END_KEY] = 36*60 + 1
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 36*60 + 2
    audio_segment_dict[SEGMENT_END_KEY] = 36*60 + 37
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 36*60 + 38
    audio_segment_dict[SEGMENT_END_KEY] = 36*60 + 53
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 36*60 + 54
    audio_segment_dict[SEGMENT_END_KEY] = 38*60
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 38*60 + 1
    audio_segment_dict[SEGMENT_END_KEY] = 38*60 + 15
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 38*60 + 15
    audio_segment_dict[SEGMENT_END_KEY] = 39*60 + 9 
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 39*60 + 9 
    audio_segment_dict[SEGMENT_END_KEY] = 39*60 + 17
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] =  39*60 + 18
    audio_segment_dict[SEGMENT_END_KEY] =  39*60 + 56
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 39*60 + 57
    audio_segment_dict[SEGMENT_END_KEY] = 40*60 + 43
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    audio_segment_dict[SEGMENT_START_KEY] = 40*60 + 43
    audio_segment_dict[SEGMENT_END_KEY] = 41*60 + 59
    audio_segments.append(audio_segment_dict)
 
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 41*60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 42*60 + 3
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pinna_Laura'
    audio_segment_dict[SEGMENT_START_KEY] = 42*60 + 2
    audio_segment_dict[SEGMENT_END_KEY] = 43*60 + 3
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    audio_segment_dict[SEGMENT_START_KEY] = 43*60 + 3
    audio_segment_dict[SEGMENT_END_KEY] = 44*60 + 4
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 44*60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 44*60 + 11
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Giagnoli_Gerardo'
    audio_segment_dict[SEGMENT_START_KEY] = 44*60 + 12
    audio_segment_dict[SEGMENT_END_KEY] = 44*60 + 43
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 44*60 + 43
    audio_segment_dict[SEGMENT_END_KEY] = 44*60 + 58
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 44*60 + 59
    audio_segment_dict[SEGMENT_END_KEY] = 46*60 + 4
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 46*60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 46*60 + 18
    audio_segments.append(audio_segment_dict)     
 
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 46*60 + 19 
    audio_segment_dict[SEGMENT_END_KEY] = 46*60 + 51
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 46*60 + 51
    audio_segment_dict[SEGMENT_END_KEY] = 47*60 + 5
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 50*60 + 31
    audio_segment_dict[SEGMENT_END_KEY] = 51*60 + 5
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 51*60 + 5
    audio_segment_dict[SEGMENT_END_KEY] = 52*60 + 1
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 52*60 + 1
    audio_segment_dict[SEGMENT_END_KEY] = 52*60 + 25
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Vacca_Elias'
    audio_segment_dict[SEGMENT_START_KEY] = 52*60 + 28
    audio_segment_dict[SEGMENT_END_KEY] = 56*60 + 7
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 56*60 + 7
    audio_segment_dict[SEGMENT_END_KEY] = 56*60 + 38
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 56*60 + 40
    audio_segment_dict[SEGMENT_END_KEY] = 57*60 + 22
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 57*60 + 22
    audio_segment_dict[SEGMENT_END_KEY] = 57*60 + 26
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 57*60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 57*60 + 56
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 57*60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 58*60 + 18
    audio_segments.append(audio_segment_dict) 

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sassu_Mario'
    audio_segment_dict[SEGMENT_START_KEY] = 58*60 + 19
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 2*60 + 43 
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 2*60 + 43  
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 3*60 + 5 
    audio_segments.append(audio_segment_dict)
    
    # Pubblicita'
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 2
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 5*60 + 25
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 5*60 + 26
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 15
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 16
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 6*60 + 21
    audio_segments.append(audio_segment_dict)  

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 6*60 + 21
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 7*60 + 8
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 7*60 + 9
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 49
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 49
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 8*60 + 56
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 8*60 + 56
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 10*60 + 40
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 10*60 + 40
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 10*60 + 51
    audio_segments.append(audio_segment_dict) 

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 10*60 + 52
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 11*60 + 4
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 11*60 + 4
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 11*60 + 6
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Polo_Marinella'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 11*60 + 7
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 12*60
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 12*60 + 1
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 12*60 + 27
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 12*60 + 27
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 14*60 + 54
    audio_segments.append(audio_segment_dict)  
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 14*60 + 54
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 15*60 + 5
    audio_segments.append(audio_segment_dict)
    
    # Pubblicita'   
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 33
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 47
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 47
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 53
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 53
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 18*60 + 57
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 18*60 + 57
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 19*60 + 41
    audio_segments.append(audio_segment_dict) 

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 19*60 + 42
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 19*60 + 52
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Sanna_Luisa'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 19*60 + 52
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 20*60 + 20
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 20*60 + 21
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 20*60 + 38
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'De_Berardinis_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 20*60 + 39
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 32
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 33
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 22*60 + 41
    audio_segments.append(audio_segment_dict)  

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'De_Berardinis_Gianni'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 22*60 + 41
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 26
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 28
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 23*60 + 46
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Pisano_Francesco'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 23*60 + 46
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 24*60 + 47
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 24*60 + 48
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 25*60 + 15
    audio_segments.append(audio_segment_dict)
    
    # Review fino a 1h 25 minuti
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Luciano_Nicola'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 25*60 + 14
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 26*60 + 59
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Minutti_Giampaola'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 35
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 36
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 27*60 + 41
    audio_segments.append(audio_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = 'Corona_Giorgia'
    audio_segment_dict[SEGMENT_START_KEY] = 3600 + 27*60 + 42
    audio_segment_dict[SEGMENT_END_KEY] = 3600 + 28*60 + 25
    audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    #audio_segment_dict[SEGMENT_START_KEY] = 3600 + 28*60 + 25
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)  

    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict)
    
    #audio_segment_dict = {}
    #audio_segment_dict[ANN_TAG_KEY] = ''
    #audio_segment_dict[SEGMENT_START_KEY] = 
    #audio_segment_dict[SEGMENT_END_KEY] = 
    #audio_segments.append(audio_segment_dict) 

    '''
    Templates
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = ''
    video_segment_dict[SEGMENT_START_KEY] = 3600 + 
    video_segment_dict[SEGMENT_END_KEY] = 3600 +
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = ''
    audio_segment_dict[SEGMENT_START_KEY] = 
    audio_segment_dict[SEGMENT_END_KEY] = 
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = ''
    caption_segment_dict[SEGMENT_START_KEY] = 
    caption_segment_dict[SEGMENT_END_KEY] =  
    caption_segments.append(caption_segment_dict)
    '''
    
    ann_dict = {}
    
    # Add durations for video segments
       
    new_video_segments = []
    
    tot_segment_duration = 0
       
    for video_segment in video_segments:
        
        new_video_segment =  {}
        ann_tag = video_segment[ANN_TAG_KEY]
        start_time = video_segment[SEGMENT_START_KEY]
        end_time = video_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        
        if(duration < 0):
            
            print('Warning! Negative duration!')
            print('ann_tag', ann_tag)
            print('start_time', start_time)
            print('end_time', end_time)
        
        tot_segment_duration = tot_segment_duration + duration
        new_video_segment[ANN_TAG_KEY] = ann_tag   
        # Transform seconds in milliseconds
        new_video_segment[SEGMENT_START_KEY] = start_time
        new_video_segment[SEGMENT_DURATION_KEY] = duration       
        new_video_segment[SEGMENT_START_KEY] = start_time * 1000
        new_video_segment[SEGMENT_DURATION_KEY] = duration * 1000
        new_video_segments.append(new_video_segment)
    
    ann_dict[VIDEO_SEGMENTS_KEY] = new_video_segments
    
    ann_dict[TOT_SEGMENT_DURATION_KEY] = tot_segment_duration
    
    # Add durations for audio and caption segments
    
    for i in range(0, len(audio_segments)):
        audio_segment = audio_segments[i]
        start_time = audio_segment[SEGMENT_START_KEY]
        end_time = audio_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        audio_segments[i][SEGMENT_DURATION_KEY] = duration
        
    for i in range(0, len(caption_segments)):
        caption_segment = caption_segments[i]
        start_time = caption_segment[SEGMENT_START_KEY]
        end_time = caption_segment[SEGMENT_END_KEY]
        duration = end_time - start_time
        caption_segments[i][SEGMENT_DURATION_KEY] = duration
        
    ann_dict[AUDIO_SEGMENTS_KEY] = audio_segments
    ann_dict[CAPTION_SEGMENTS_KEY] = caption_segments
    
    save_YAML_file(file_path, ann_dict)
    
    return ann_dict


def make_MONITOR272010_annotations(file_path):
    '''
    Make annotations for MONITOR272010.mpg video file
    
    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    '''
    
    audio_segments = []
    caption_segments = []
    video_segments = []
    '''
    Templates
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = ''
    video_segment_dict[SEGMENT_START_KEY] = 
    video_segment_dict[SEGMENT_END_KEY] = 
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = ''
    audio_segment_dict[SEGMENT_START_KEY] = 
    audio_segment_dict[SEGMENT_END_KEY] = 
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = ''
    caption_segment_dict[SEGMENT_START_KEY] = 
    caption_segment_dict[SEGMENT_END_KEY] =  
    caption_segments.append(caption_segment_dict)
    '''
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 60 + 59
    video_segments.append(video_segment_dict) 
     
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    caption_segment_dict[SEGMENT_START_KEY] = 60 + 48
    caption_segment_dict[SEGMENT_END_KEY] =  60 + 52
    caption_segments.append(caption_segment_dict)   

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 3
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 3
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 8
    video_segments.append(video_segment_dict)   
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Argiolas_Valentina'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 8
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 11
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 14
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Murrocu_Maria_Grazia'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 17
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 17
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 22
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Picciau_Gigi'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 24
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 28
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 34
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 55
    video_segment_dict[SEGMENT_END_KEY] = 2*60 + 59
    video_segments.append(video_segment_dict)     
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sechi_Egidiangela'
    video_segment_dict[SEGMENT_START_KEY] = 2*60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 3*60 + 10
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 3*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 4*60 + 21
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 4*60 + 25
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 14
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    caption_segment_dict[SEGMENT_START_KEY] = 4*60 + 31
    caption_segment_dict[SEGMENT_END_KEY] =  4*60 + 38
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 17
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 17
    video_segment_dict[SEGMENT_END_KEY] = 5*60 + 52
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    caption_segment_dict[SEGMENT_START_KEY] = 5*60 + 24
    caption_segment_dict[SEGMENT_END_KEY] = 5*60 + 31
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 5*60 + 52
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 1
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 1
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 7
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 14
    video_segment_dict[SEGMENT_END_KEY] = 6*60 + 46
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 6*60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 10
    video_segments.append(video_segment_dict) 
        
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 20
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Picciau_Gigi'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 7*60 + 28
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Picciau_Gigi'
    video_segment_dict[SEGMENT_START_KEY] = 7*60 + 33
    video_segment_dict[SEGMENT_END_KEY] = 8*60 + 17
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Picciau_Gigi'
    caption_segment_dict[SEGMENT_START_KEY] = 7*60 + 37
    caption_segment_dict[SEGMENT_END_KEY] =  7*60 + 44
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 8*60 + 20
    video_segment_dict[SEGMENT_END_KEY] = 8*60 + 25
    video_segments.append(video_segment_dict)     

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Murrocu_Maria_Grazia'
    video_segment_dict[SEGMENT_START_KEY] = 8*60 + 29
    video_segment_dict[SEGMENT_END_KEY] = 8*60 + 49
    video_segments.append(video_segment_dict)   

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Murrocu_Maria_Grazia'
    caption_segment_dict[SEGMENT_START_KEY] = 8*60 + 35
    caption_segment_dict[SEGMENT_END_KEY] =  8*60 + 42
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 8*60 + 49
    video_segment_dict[SEGMENT_END_KEY] = 8*60 + 59
    video_segments.append(video_segment_dict)   

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Argiolas_Valentina'
    video_segment_dict[SEGMENT_START_KEY] = 8*60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 9*60 + 23
    video_segments.append(video_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Argiolas_Valentina'
    caption_segment_dict[SEGMENT_START_KEY] = 9*60 + 3
    caption_segment_dict[SEGMENT_END_KEY] = 9*60 + 11
    caption_segments.append(caption_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 9*60 + 23
    video_segment_dict[SEGMENT_END_KEY] = 9*60 + 33
    video_segments.append(video_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Sechi_Egidiangela'
    caption_segment_dict[SEGMENT_START_KEY] = 10 *60
    caption_segment_dict[SEGMENT_END_KEY] = 10*60 + 7 
    caption_segments.append(caption_segment_dict)    
          
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Sechi_Egidiangela'
    video_segment_dict[SEGMENT_START_KEY] = 10*60 + 51
    video_segment_dict[SEGMENT_END_KEY] = 10*60 + 54
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 10*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 11*60 + 2
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 6
    video_segment_dict[SEGMENT_END_KEY] = 11*60 + 27
    video_segments.append(video_segment_dict)
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 11*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 11*60 + 42
    video_segments.append(video_segment_dict)        

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 15*60 + 18
    video_segment_dict[SEGMENT_END_KEY] = 15*60 + 43
    video_segments.append(video_segment_dict) 
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Scalas_Marco'
    caption_segment_dict[SEGMENT_START_KEY] = 15*60 + 41
    caption_segment_dict[SEGMENT_END_KEY] = 17*60 + 12
    caption_segments.append(caption_segment_dict)    

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 15*60 + 56
    video_segment_dict[SEGMENT_END_KEY] = 16*60 + 34
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 17*60 + 11
    video_segment_dict[SEGMENT_END_KEY] = 17*60 + 23 
    video_segments.append(video_segment_dict)      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 19*60 + 57
    video_segment_dict[SEGMENT_END_KEY] = 20*60 + 19 
    video_segments.append(video_segment_dict)  

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 20*60 + 22
    video_segment_dict[SEGMENT_END_KEY] = 20*60 + 30 
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 20*60 + 36
    video_segment_dict[SEGMENT_END_KEY] = 20*60 + 49
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 22*60 + 42
    video_segment_dict[SEGMENT_END_KEY] = 22*60 + 54
    video_segments.append(video_segment_dict)      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 22*60 + 54
    video_segment_dict[SEGMENT_END_KEY] = 24*60 + 39
    video_segments.append(video_segment_dict)   

    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    caption_segment_dict[SEGMENT_START_KEY] = 23*60 + 2
    caption_segment_dict[SEGMENT_END_KEY] = 23*60 + 6
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 24*60 + 41
    video_segment_dict[SEGMENT_END_KEY] = 24*60 + 57
    video_segments.append(video_segment_dict)  
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 25*60 + 4
    video_segment_dict[SEGMENT_END_KEY] = 25*60 + 24
    video_segments.append(video_segment_dict) 
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 25*60 + 47
    video_segment_dict[SEGMENT_END_KEY] = 25*60 + 57
    video_segments.append(video_segment_dict)          

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 26*60 + 16
    video_segment_dict[SEGMENT_END_KEY] = 26*60 + 59
    video_segments.append(video_segment_dict) 
 
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 26*60 + 59
    video_segment_dict[SEGMENT_END_KEY] = 27*60 + 10
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 27*60 + 10
    video_segment_dict[SEGMENT_END_KEY] = 27*60 + 25
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 27*60 + 31
    video_segment_dict[SEGMENT_END_KEY] = 28*60 + 12
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Prato_Andrea'
    video_segment_dict[SEGMENT_START_KEY] = 28*60 + 19
    video_segment_dict[SEGMENT_END_KEY] = 28*60 + 26
    video_segments.append(video_segment_dict)

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 28*60 + 28
    video_segment_dict[SEGMENT_END_KEY] = 28*60 + 35
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 32*60 + 56
    video_segment_dict[SEGMENT_END_KEY] = 33*60 + 6
    video_segments.append(video_segment_dict) 

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Dessi_Emanuele'
    video_segment_dict[SEGMENT_START_KEY] = 33*60 + 24
    video_segment_dict[SEGMENT_END_KEY] = 33*60 + 34
    video_segments.append(video_segment_dict)                      

    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    video_segment_dict[SEGMENT_START_KEY] = 33*60 + 35
    video_segment_dict[SEGMENT_END_KEY] = 33*60 + 40
    video_segments.append(video_segment_dict)

    #video_segment_dict = {}
    #video_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    #video_segment_dict[SEGMENT_START_KEY] = 33*60 + 48
    #video_segment_dict[SEGMENT_END_KEY] = 
    #video_segments.append(video_segment_dict)

    #caption_segment_dict = {}
    #caption_segment_dict[ANN_TAG_KEY] = 'Ladu_Fortunato'
    #caption_segment_dict[SEGMENT_START_KEY] = 33*60 + 55
    #caption_segment_dict[SEGMENT_END_KEY] =  
    #caption_segments.append(caption_segment_dict)
    '''
    Templates
    
    video_segment_dict = {}
    video_segment_dict[ANN_TAG_KEY] = ''
    video_segment_dict[SEGMENT_START_KEY] = 
    video_segment_dict[SEGMENT_END_KEY] = 
    video_segments.append(video_segment_dict)
    
    audio_segment_dict = {}
    audio_segment_dict[ANN_TAG_KEY] = ''
    audio_segment_dict[SEGMENT_START_KEY] = 
    audio_segment_dict[SEGMENT_END_KEY] = 
    audio_segments.append(audio_segment_dict)
    
    caption_segment_dict = {}
    caption_segment_dict[ANN_TAG_KEY] = ''
    caption_segment_dict[SEGMENT_START_KEY] = 
    caption_segment_dict[SEGMENT_END_KEY] =  
    caption_segments.append(caption_segment_dict)
    '''                                                                      
     
def calculate_stats(ann_dict):
    '''
    Calculate statistics for tags in dictionary with annotations
    
    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video
    '''
    tags = get_tags(ann_dict)
    
    tags_list = []
    for tag in sorted(tags):
        
        tag_dict = {}
        tag_dict[ANN_TAG_KEY] = tag
        person_dict = get_video_annotations_for_person(ann_dict, tag)
        dur = person_dict[TOT_SEGMENT_DURATION_KEY]
        tag_dict[TOT_SEGMENT_DURATION_KEY] = dur
        segments_nr = person_dict[SEGMENTS_NR_KEY]
        tag_dict[SEGMENTS_NR_KEY] = segments_nr
        tags_list.append(tag_dict)
        
        print(tag_dict)
        
        
def get_tags(ann_dict):
    '''
    Get list of tags in dictionary with annotations
    
    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video

    '''
    
    tags = []
    video_segments = ann_dict[VIDEO_SEGMENTS_KEY]
    
    for i in range(0, len(video_segments)):
        
        ann_tag = video_segments[i][ANN_TAG_KEY]
        
        if(not(ann_tag in tags)):
            
            tags.append(ann_tag)
            
    return tags     
            
    
def get_video_annotations_for_person(ann_dict, person_tag):
    '''
    Get video annotations for given person
    
    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video
    
    :type person_tag: string
    :param person_tag: tag of person
    ''' 
    
    person_dict = {}
    
    person_dict[ANN_TAG_KEY] = person_tag
    
    person_segments =  []
    
    video_segments = ann_dict[VIDEO_SEGMENTS_KEY]
    
    tot_duration = 0
    
    for video_segment in video_segments:
        
        ann_tag = video_segment[ANN_TAG_KEY]
        
        if(ann_tag == person_tag):
            
            new_person_segment = {}
            
            start = video_segment[SEGMENT_START_KEY]
            
            new_person_segment[SEGMENT_START_KEY] = start
            
            duration = video_segment[SEGMENT_DURATION_KEY] 
            
            tot_duration = tot_duration + duration
            
            new_person_segment[SEGMENT_DURATION_KEY] = duration 
            
            person_segments.append(new_person_segment)
            
    person_dict[SEGMENTS_KEY] = person_segments 
    
    person_dict[SEGMENTS_NR_KEY] = len(person_segments)       
            
    person_dict[TOT_SEGMENT_DURATION_KEY] = tot_duration
            
    return person_dict
    
    
def save_people_files(ann_dict, video_ann_file_path):
    '''
    Save files with the annotations for each people
    
    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video
    
    :video_ann_file_path: string
    :video_ann_file_path: path of file with annotations for whole video
    ''' 
    
    tags = get_tags(ann_dict)
    print(tags)
    
    for tag in tags:
        
        person_dict = get_video_annotations_for_person(ann_dict, tag)
        
        file_name = tag + '.YAML'
        
        file_path = os.path.join(video_ann_file_path, file_name)
        
        save_YAML_file(file_path, person_dict)
               
    
#video_dir = os.path.join(VIDEO_ANN_PATH, 'MONITOR072011')    
    
#file_path_no_ext = os.path.join(video_dir, 'MONITOR072011.mp4')

#file_path = file_path_no_ext + '.YAML'
    
#ann_dict = make_MONITOR072011_annotations(file_path)

#save_people_files(ann_dict, video_dir)

#file_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-15V\Annotations\MONITOR072011.YAML'

#ann_dict = make_MONITOR072011_annotations(file_path)

#calculate_stats(ann_dict)

file_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\fic.02.yml'

ann_dict = make_fic02_annotations(file_path)

save_people_files(ann_dict, r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations')
    
    
