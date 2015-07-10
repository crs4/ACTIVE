import os
import sys
sys.path.append("..")
import tools.constants as c
from tools.utils import save_YAML_file


def transform_segments(segments):
    """
    Add duration to segments and convert seconds in milliseconds

    :type segments: list
    :param segments: list of segments

    :rtype integer
    :returns: total duration of segments
    """

    tot_segment_duration = 0

    for segment in segments:

        ann_tag = segment[c.ANN_TAG_KEY]

        # Add duration
        start_time = segment[c.SEGMENT_START_KEY]
        end_time = segment[c.SEGMENT_END_KEY]
        duration = end_time - start_time

        if duration < 0:

            print('Warning! Negative duration!')
            print('ann_tag', ann_tag)
            print('start_time', start_time)
            print('end_time', end_time)

        tot_segment_duration = tot_segment_duration + duration
        # transform seconds in milliseconds
        segment[c.SEGMENT_START_KEY] = start_time * 1000
        segment[c.SEGMENT_DURATION_KEY] = duration * 1000

    return tot_segment_duration


def make_fic02_annotations(file_path):
    """
    Make annotations for fic.02.mpg video file

    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    """

    audio_segments = []
    caption_segments = []
    video_segments = []

    video_segment_dict = {c.SEGMENT_START_KEY: 53,
                          c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_END_KEY: 2 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 2 * 60 + 42,
                          c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_END_KEY: 2 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 2 * 60 + 49,
                          c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_END_KEY: 2 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 2 * 60 + 59,
                          c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_END_KEY: 3 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 3 * 60 + 27,
                          c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_END_KEY: 3 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 4 * 60 + 30,
                          c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_END_KEY: 4 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 5 * 60 + 30,
                          c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_END_KEY: 6 * 60 + 40}
    video_segments.append(video_segment_dict)

    # Tutti e 3 gli ospiti

    video_segment_dict = {c.SEGMENT_START_KEY: 6 * 60 + 40,
                          c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_END_KEY: 6 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 6 * 60 + 40,
                          c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_END_KEY: 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.SEGMENT_START_KEY: 6 * 60 + 40,
                          c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_END_KEY: 6 * 60 + 58}
    video_segments.append(video_segment_dict)


    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 54,
                          c.SEGMENT_END_KEY: 6 * 60 + 51}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                            c.SEGMENT_START_KEY: 63, c.SEGMENT_END_KEY: 67}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 6 * 60 + 40,
                          c.SEGMENT_END_KEY: 7 * 60 + 28}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                            c.SEGMENT_START_KEY: 7 * 60 + 3,
                            c.SEGMENT_END_KEY: 7 * 60 + 9}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 7 * 60 + 27,
                          c.SEGMENT_END_KEY: 7 * 60 + 33}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 7 * 60 + 28,
                          c.SEGMENT_END_KEY: 7 * 60 + 33}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                            c.SEGMENT_START_KEY: 7 * 60 + 37,
                            c.SEGMENT_END_KEY: 7 * 60 + 43}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 7 * 60 + 33,
                          c.SEGMENT_END_KEY: 8 * 60 + 37}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 7 * 60 + 33,
                          c.SEGMENT_END_KEY: 7 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 8 * 60 + 2,
                          c.SEGMENT_END_KEY: 8 * 60 + 38}
    video_segments.append(video_segment_dict)


    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 8 * 60 + 37,
                          c.SEGMENT_END_KEY: 8 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 8 * 60 + 38,
                          c.SEGMENT_END_KEY: 8 * 60 + 46}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 8 * 60 + 46,
                          c.SEGMENT_END_KEY: 9 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 8 * 60 + 46,
                          c.SEGMENT_END_KEY: 9 * 60 + 5}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 9 * 60 + 32,
                          c.SEGMENT_END_KEY: 9 * 60 + 54}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 9 * 60 + 32,
                          c.SEGMENT_END_KEY: 9 * 60 + 54}
    video_segments.append(video_segment_dict)

    # Interviste per strada

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 9 * 60 + 56,
                          c.SEGMENT_END_KEY: 9 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 10 * 60 + 12,
                          c.SEGMENT_END_KEY: 10 * 60 + 14}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 10 * 60 + 20,
                          c.SEGMENT_END_KEY: 10 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 10 * 60 + 35,
                          c.SEGMENT_END_KEY: 10 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 10 * 60 + 45,
                          c.SEGMENT_END_KEY: 10 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 10 * 60 + 57,
                          c.SEGMENT_END_KEY: 10 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 11 * 60 + 11,
                          c.SEGMENT_END_KEY: 11 * 60 + 12}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 11 * 60 + 31,
                          c.SEGMENT_END_KEY: 11 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 11 * 60 + 42,
                          c.SEGMENT_END_KEY: 11 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 11 * 60 + 46,
                          c.SEGMENT_END_KEY: 11 * 60 + 47}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 12 * 60 + 11,
                          c.SEGMENT_END_KEY: 12 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 12 * 60 + 33,
                          c.SEGMENT_END_KEY: 12 * 60 + 35}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 12 * 60 + 50,
                          c.SEGMENT_END_KEY: 12 * 60 + 52}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 13 * 60 + 16,
                          c.SEGMENT_END_KEY: 13 * 60 + 21}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 13 * 60 + 52,
                          c.SEGMENT_END_KEY: 13 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    # Ritorno in studio

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 14 * 60 + 17,
                          c.SEGMENT_END_KEY: 14 * 60 + 24}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 14 * 60 + 17,
                          c.SEGMENT_END_KEY: 14 * 60 + 24}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 14 * 60 + 24,
                          c.SEGMENT_END_KEY: 15 * 60 + 3}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 14 * 60 + 24,
                          c.SEGMENT_END_KEY: 14 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 14 * 60 + 24,
                          c.SEGMENT_END_KEY: 14 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 14 * 60 + 24,
                          c.SEGMENT_END_KEY: 15 * 60 + 4}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                            c.SEGMENT_START_KEY: 14 * 60 + 34,
                            c.SEGMENT_END_KEY: 14 * 60 + 39}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 15 * 60 + 3,
                          c.SEGMENT_END_KEY: 15 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 15 * 60 + 6,
                          c.SEGMENT_END_KEY: 15 * 60 + 27}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 15 * 60 + 6,
                          c.SEGMENT_END_KEY: 15 * 60 + 27}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                            c.SEGMENT_START_KEY: 15 * 60 + 9,
                            c.SEGMENT_END_KEY: 15 * 60 + 14}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 15 * 60 + 26,
                          c.SEGMENT_END_KEY: 15 * 60 + 28}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 15 * 60 + 29,
                          c.SEGMENT_END_KEY: 16 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 15 * 60 + 36,
                          c.SEGMENT_END_KEY: 15 * 60 + 52}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                            c.SEGMENT_START_KEY: 15 * 60 + 39,
                            c.SEGMENT_END_KEY: 15 * 60 + 44}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 15 * 60 + 58,
                          c.SEGMENT_END_KEY: 16 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 16 * 60 + 3,
                          c.SEGMENT_END_KEY: 16 * 60 + 7}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 16 * 60 + 5,
                          c.SEGMENT_END_KEY: 16 * 60 + 9}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 16 * 60 + 5,
                          c.SEGMENT_END_KEY: 16 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 16 * 60 + 42,
                          c.SEGMENT_END_KEY: 16 * 60 + 49}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 16 * 60 + 40,
                          c.SEGMENT_END_KEY: 16 * 60 + 44}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 11,
                          c.SEGMENT_END_KEY: 17 * 60 + 17}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 11,
                          c.SEGMENT_END_KEY: 17 * 60 + 13}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 17 * 60 + 13,
                          c.SEGMENT_END_KEY: 17 * 60 + 34}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 17 * 60 + 17,
                          c.SEGMENT_END_KEY: 17 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 34,
                          c.SEGMENT_END_KEY: 17 * 60 + 38}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 34,
                          c.SEGMENT_END_KEY: 17 * 60 + 38}
    audio_segments.append(audio_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 18 * 60,
                          c.SEGMENT_END_KEY: 18 * 60 + 25}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 18 * 60 + 3,
                          c.SEGMENT_END_KEY: 18 * 60 + 23}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 18 * 60 + 25,
                          c.SEGMENT_END_KEY: 18 * 60 + 54}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 18 * 60 + 25,
                          c.SEGMENT_END_KEY: 19 * 60 + 11}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 18 * 60 + 54,
                          c.SEGMENT_END_KEY: 19 * 60 + 29}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                            c.SEGMENT_START_KEY: 18 * 60 + 56,
                            c.SEGMENT_END_KEY: 18 * 60 + 59}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 19 * 60 + 21,
                          c.SEGMENT_END_KEY: 19 * 60 + 31}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 20 * 60 + 4,
                          c.SEGMENT_END_KEY: 20 * 60 + 9}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 19 * 60 + 44,
                          c.SEGMENT_END_KEY: 20 * 60 + 36}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 19 * 60 + 32,
                          c.SEGMENT_END_KEY: 20 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 20 * 60 + 29,
                          c.SEGMENT_END_KEY: 20 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 20 * 60 + 57,
                          c.SEGMENT_END_KEY: 21 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                            c.SEGMENT_START_KEY: 20 * 60 + 10,
                            c.SEGMENT_END_KEY: 20 * 60 + 15}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 20 * 60 + 43,
                          c.SEGMENT_END_KEY: 21 * 60 + 15}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 21 * 60 + 4,
                          c.SEGMENT_END_KEY: 21 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 21 * 60 + 15,
                          c.SEGMENT_END_KEY: 21 * 60 + 24}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 21 * 60 + 24,
                          c.SEGMENT_END_KEY: 21 * 60 + 54}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 21 * 60 + 28,
                          c.SEGMENT_END_KEY: 21 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 21 * 60 + 38,
                          c.SEGMENT_END_KEY: 23 * 60 + 45}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 21 * 60 + 54,
                          c.SEGMENT_END_KEY: 21 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 21 * 60 + 59,
                          c.SEGMENT_END_KEY: 22 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 22 * 60 + 26,
                          c.SEGMENT_END_KEY: 24 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 24 * 60 + 22,
                          c.SEGMENT_END_KEY: 24 * 60 + 25}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 23 * 60 + 49,
                          c.SEGMENT_END_KEY: 24 * 60 + 46}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Caredda_Giorgio',
                          c.SEGMENT_START_KEY: 24 * 60 + 26,
                          c.SEGMENT_END_KEY: 24 * 60 + 31}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 24 * 60 + 49,
                          c.SEGMENT_END_KEY: 24 * 60 + 55}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 24 * 60 + 49,
                          c.SEGMENT_END_KEY: 24 * 60 + 55}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 24 * 60 + 55,
                          c.SEGMENT_END_KEY: 25 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    # I 3 ospiti in contemporanea

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 24 * 60 + 55,
                          c.SEGMENT_END_KEY: 25 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 24 * 60 + 55,
                          c.SEGMENT_END_KEY: 25 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 24 * 60 + 55,
                          c.SEGMENT_END_KEY: 25 * 60 + 45}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                            c.SEGMENT_START_KEY: 25 * 60 + 7,
                            c.SEGMENT_END_KEY: 25 * 60 + 10}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 25 * 60 + 43,
                          c.SEGMENT_END_KEY: 25 * 60 + 49}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 25 * 60 + 45,
                          c.SEGMENT_END_KEY: 25 * 60 + 49}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 26 * 60 + 8,
                          c.SEGMENT_END_KEY: 26 * 60 + 43}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 26 * 60 + 13,
                          c.SEGMENT_END_KEY: 26 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                          c.SEGMENT_START_KEY: 26 * 60 + 43,
                          c.SEGMENT_END_KEY: 31 * 60 + 35}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                          c.SEGMENT_START_KEY: 26 * 60 + 43,
                          c.SEGMENT_END_KEY: 27 * 60 + 26}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                            c.SEGMENT_START_KEY: 26 * 60 + 59,
                            c.SEGMENT_END_KEY: 27 * 60 + 5}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 27 * 60 + 26,
                          c.SEGMENT_END_KEY: 27 * 60 + 31}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                          c.SEGMENT_START_KEY: 27 * 60 + 31,
                          c.SEGMENT_END_KEY: 28 * 60 + 8}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 28 * 60 + 9,
                          c.SEGMENT_END_KEY: 28 * 60 + 20}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 29 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                            c.SEGMENT_START_KEY: 28 * 60 + 41,
                            c.SEGMENT_END_KEY: 28 * 60 + 47}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 29 * 60 + 56,
                          c.SEGMENT_END_KEY: 30 * 60 + 1}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                          c.SEGMENT_START_KEY: 30 * 60 + 2,
                          c.SEGMENT_END_KEY: 31 * 60 + 35}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Locatelli_Gianni',
                            c.SEGMENT_START_KEY: 30 * 60 + 27,
                            c.SEGMENT_END_KEY: 30 * 60 + 31}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 31 * 60 + 37,
                          c.SEGMENT_END_KEY: 31 * 60 + 43}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 31 * 60 + 38,
                          c.SEGMENT_END_KEY: 32 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    # I 3 ospiti in contemporanea

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 31 * 60 + 43,
                          c.SEGMENT_END_KEY: 31 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 31 * 60 + 43,
                          c.SEGMENT_END_KEY: 32 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 31 * 60 + 43,
                          c.SEGMENT_END_KEY: 32 * 60 + 29}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 32 * 60 + 5,
                          c.SEGMENT_END_KEY: 33 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                            c.SEGMENT_START_KEY: 32 * 60 + 21,
                            c.SEGMENT_END_KEY: 32 * 60 + 28}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 32 * 60 + 40,
                          c.SEGMENT_END_KEY: 33 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 33 * 60 + 22,
                          c.SEGMENT_END_KEY: 33 * 60 + 46}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 33 * 60 + 46,
                          c.SEGMENT_END_KEY: 33 * 60 + 50}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 33 * 60 + 46,
                          c.SEGMENT_END_KEY: 33 * 60 + 53}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 33 * 60 + 51,
                          c.SEGMENT_END_KEY: 34 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 33 * 60 + 53,
                          c.SEGMENT_END_KEY: 34 * 60 + 30}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                            c.SEGMENT_START_KEY: 34 * 60 + 14,
                            c.SEGMENT_END_KEY: 34 * 60 + 19}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 34 * 60 + 30,
                          c.SEGMENT_END_KEY: 34 * 60 + 56}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 34 * 60 + 43,
                          c.SEGMENT_END_KEY: 34 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 34 * 60 + 56,
                          c.SEGMENT_END_KEY: 35 * 60 + 6}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 34 * 60 + 59,
                          c.SEGMENT_END_KEY: 35 * 60 + 3}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 35 * 60 + 3,
                          c.SEGMENT_END_KEY: 35 * 60 + 24}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 35 * 60 + 8,
                          c.SEGMENT_END_KEY: 35 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 35 * 60 + 14,
                          c.SEGMENT_END_KEY: 35 * 60 + 24}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 35 * 60 + 27,
                          c.SEGMENT_END_KEY: 35 * 60 + 53}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 35 * 60 + 53,
                          c.SEGMENT_END_KEY: 35 * 60 + 57}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 35 * 60 + 57,
                          c.SEGMENT_END_KEY: 36 * 60 + 9}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 35 * 60 + 36,
                          c.SEGMENT_END_KEY: 36 * 60 + 9}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                            c.SEGMENT_START_KEY: 35 * 60 + 38,
                            c.SEGMENT_END_KEY: 35 * 60 + 43}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 36 * 60 + 9,
                          c.SEGMENT_END_KEY: 36 * 60 + 14}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 36 * 60 + 8,
                          c.SEGMENT_END_KEY: 36 * 60 + 14}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 36 * 60 + 14,
                          c.SEGMENT_END_KEY: 36 * 60 + 37}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 36 * 60 + 14,
                          c.SEGMENT_END_KEY: 36 * 60 + 37}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                            c.SEGMENT_START_KEY: 36 * 60 + 18,
                            c.SEGMENT_END_KEY: 36 * 60 + 22}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 36 * 60 + 37,
                          c.SEGMENT_END_KEY: 36 * 60 + 45}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 36 * 60 + 37,
                          c.SEGMENT_END_KEY: 36 * 60 + 42}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 36 * 60 + 50,
                          c.SEGMENT_END_KEY: 37 * 60 + 2}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 37 * 60 + 2,
                          c.SEGMENT_END_KEY: 37 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 37 * 60 + 4,
                          c.SEGMENT_END_KEY: 37 * 60 + 34}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 36 * 60 + 52,
                          c.SEGMENT_END_KEY: 37 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 37 * 60 + 4,
                          c.SEGMENT_END_KEY: 37 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 37 * 60 + 8,
                          c.SEGMENT_END_KEY: 37 * 60 + 37}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 37 * 60 + 34,
                          c.SEGMENT_END_KEY: 37 * 60 + 38}
    audio_segments.append(audio_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 38 * 60 + 1,
                          c.SEGMENT_END_KEY: 38 * 60 + 20}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 38 * 60 + 3,
                          c.SEGMENT_END_KEY: 38 * 60 + 51}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 38 * 60 + 20,
                          c.SEGMENT_END_KEY: 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 38 * 60 + 20,
                          c.SEGMENT_END_KEY: 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 38 * 60 + 20,
                          c.SEGMENT_END_KEY: 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 38 * 60 + 30,
                          c.SEGMENT_END_KEY: 38 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 38 * 60 + 51,
                          c.SEGMENT_END_KEY: 39 * 60 + 10}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 38 * 60 + 51,
                          c.SEGMENT_END_KEY: 40 * 60 + 54}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 39 * 60 + 16,
                          c.SEGMENT_END_KEY: 40 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 39 * 60 + 50,
                          c.SEGMENT_END_KEY: 40 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 39 * 60 + 54,
                          c.SEGMENT_END_KEY: 40 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 40 * 60 + 25,
                          c.SEGMENT_END_KEY: 40 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 40 * 60 + 30,
                          c.SEGMENT_END_KEY: 40 * 60 + 54}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 40 * 60 + 54,
                          c.SEGMENT_END_KEY: 41 * 60 + 14}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 40 * 60 + 54,
                          c.SEGMENT_END_KEY: 41 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 41 * 60 + 3,
                          c.SEGMENT_END_KEY: 41 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 41 * 60 + 3,
                          c.SEGMENT_END_KEY: 41 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 41 * 60 + 3,
                          c.SEGMENT_END_KEY: 41 * 60 + 19}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 41 * 60 + 14,
                          c.SEGMENT_END_KEY: 41 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 41 * 60 + 38,
                          c.SEGMENT_END_KEY: 41 * 60 + 42}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 41 * 60 + 40,
                          c.SEGMENT_END_KEY: 41 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 41 * 60 + 47,
                          c.SEGMENT_END_KEY: 42 * 60 + 3}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 41 * 60 + 42,
                          c.SEGMENT_END_KEY: 42 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 42 * 60 + 11,
                          c.SEGMENT_END_KEY: 42 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 42 * 60 + 11,
                          c.SEGMENT_END_KEY: 42 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 42 * 60 + 11,
                          c.SEGMENT_END_KEY: 42 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 42 * 60 + 37,
                          c.SEGMENT_END_KEY: 42 * 60 + 50}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 42 * 60 + 41,
                          c.SEGMENT_END_KEY: 42 * 60 + 45}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 42 * 60 + 58,
                          c.SEGMENT_END_KEY: 43 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 42 * 60 + 59,
                          c.SEGMENT_END_KEY: 43 * 60 + 46}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 42 * 60 + 56,
                          c.SEGMENT_END_KEY: 43 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 43 * 60 + 46,
                          c.SEGMENT_END_KEY: 43 * 60 + 57}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 43 * 60 + 46,
                          c.SEGMENT_END_KEY: 44 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 43 * 60 + 57,
                          c.SEGMENT_END_KEY: 43 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 43 * 60 + 57,
                          c.SEGMENT_END_KEY: 44 * 60}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni Mario',
                          c.SEGMENT_START_KEY: 44 * 60 + 6,
                          c.SEGMENT_END_KEY: 44 * 60 + 19}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 44 * 60 + 10,
                          c.SEGMENT_END_KEY: 44 * 60 + 45}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 44 * 60 + 19,
                          c.SEGMENT_END_KEY: 44 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 44 * 60 + 21,
                          c.SEGMENT_END_KEY: 45 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 45 * 60 + 39,
                          c.SEGMENT_END_KEY: 45 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 45 * 60 + 46,
                          c.SEGMENT_END_KEY: 47 * 60 + 10}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 47 * 60 + 10,
                          c.SEGMENT_END_KEY: 47 * 60 + 23}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 47 * 60 + 23,
                          c.SEGMENT_END_KEY: 47 * 60 + 36}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 47 * 60 + 36,
                          c.SEGMENT_END_KEY: 47 * 60 + 45}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 47 * 60 + 45,
                          c.SEGMENT_END_KEY: 48 * 60 + 10}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 48 * 60 + 10,
                          c.SEGMENT_END_KEY: 48 * 60 + 12}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Leoni_Mario',
                          c.SEGMENT_START_KEY: 48 * 60 + 12,
                          c.SEGMENT_END_KEY: 49 * 60 + 45}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 48 * 60 + 42,
                          c.SEGMENT_END_KEY: 48 * 60 + 51}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 49 * 60 + 6,
                          c.SEGMENT_END_KEY: 49 * 60 + 8}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 49 * 60 + 45,
                          c.SEGMENT_END_KEY: 49 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 50 * 60 + 5,
                          c.SEGMENT_END_KEY: 50 * 60 + 16}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 50 * 60 + 14,
                          c.SEGMENT_END_KEY: 51 * 60 + 2}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 50 * 60 + 12,
                          c.SEGMENT_END_KEY: 51 * 60 + 3}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                            c.SEGMENT_START_KEY: 50 * 60 + 19,
                            c.SEGMENT_END_KEY: 50 * 60 + 25}
    caption_segments.append(caption_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 51 * 60 + 3,
                          c.SEGMENT_END_KEY: 51 * 60 + 20}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 51 * 60 + 4,
                          c.SEGMENT_END_KEY: 51 * 60 + 21}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 51 * 60 + 20,
                          c.SEGMENT_END_KEY: 52 * 60 + 44}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                          c.SEGMENT_START_KEY: 51 * 60 + 21,
                          c.SEGMENT_END_KEY: 52 * 60 + 44}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fadda_Paolo',
                            c.SEGMENT_START_KEY: 51 * 60 + 23,
                            c.SEGMENT_END_KEY: 51 * 60 + 30}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giannotta_Michele',
                          c.SEGMENT_START_KEY: 52 * 60 + 21,
                          c.SEGMENT_END_KEY: 52 * 60 + 44}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 52 * 60 + 44,
                          c.SEGMENT_END_KEY: 53 * 60 + 2}
    audio_segments.append(audio_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 52 * 60 + 44,
                          c.SEGMENT_END_KEY: 53 * 60 + 4}
    video_segments.append(video_segment_dict)

    # Add durations for video and caption segments,
    # transform seconds in milliseconds
    tot_video_segment_duration = transform_segments(video_segments)
    tot_caption_segment_duration = transform_segments(caption_segments)

    ann_dict = {
        c.VIDEO_SEGMENTS_KEY: video_segments,
        c.TOT_SEGMENT_DURATION_KEY: tot_video_segment_duration,
        c.CAPTION_SEGMENTS_KEY: caption_segments,
        c.TOT_CAPTION_SEGMENT_DURATION_KEY: tot_caption_segment_duration
    }

    # Create necessary directories and save YAML file
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_YAML_file(file_path, ann_dict)

    return ann_dict


def make_fic03_annotations(file_path):
    """
    Make annotations for Fic.03.mpg video file

    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    """

    caption_segments = []
    video_segments = []

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 44,
                          c.SEGMENT_END_KEY: 2 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 3 * 60 + 16,
                          c.SEGMENT_END_KEY: 3 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 3 * 60 + 40,
                          c.SEGMENT_END_KEY: 4 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 4 * 60 + 1,
                          c.SEGMENT_END_KEY: 4 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 4 * 60 + 5,
                          c.SEGMENT_END_KEY: 4 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 4 * 60 + 17,
                          c.SEGMENT_END_KEY: 4 * 60 + 48}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                            c.SEGMENT_START_KEY: 4 * 60 + 33,
                            c.SEGMENT_END_KEY: 4 * 60 + 41}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 4 * 60 + 48,
                          c.SEGMENT_END_KEY: 5 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 5 * 60 + 1,
                          c.SEGMENT_END_KEY: 5 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 5 * 60 + 3,
                          c.SEGMENT_END_KEY: 5 * 60 + 16}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                            c.SEGMENT_START_KEY: 5 * 60 + 5,
                            c.SEGMENT_END_KEY: 5 * 60 + 8}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 5 * 60 + 16,
                          c.SEGMENT_END_KEY: 5 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 5 * 60 + 35,
                          c.SEGMENT_END_KEY: 5 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 12 * 60 + 16,
                          c.SEGMENT_END_KEY: 12 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 13 * 60 + 16,
                          c.SEGMENT_END_KEY: 13 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 13 * 60 + 21,
                          c.SEGMENT_END_KEY: 13 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 13 * 60 + 21,
                          c.SEGMENT_END_KEY: 13 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 13 * 60 + 21,
                          c.SEGMENT_END_KEY: 14 * 60 + 18}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                            c.SEGMENT_START_KEY: 13 * 60 + 39,
                            c.SEGMENT_END_KEY: 13 * 60 + 45}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 14 * 60 + 18,
                          c.SEGMENT_END_KEY: 14 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 14 * 60 + 23,
                          c.SEGMENT_END_KEY: 14 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 14 * 60 + 46,
                          c.SEGMENT_END_KEY: 14 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 14 * 60 + 52,
                          c.SEGMENT_END_KEY: 15 * 60 + 16}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                            c.SEGMENT_START_KEY: 14 * 60 + 54,
                            c.SEGMENT_END_KEY: 15 * 60}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 15 * 60 + 21,
                          c.SEGMENT_END_KEY: 15 * 60 + 56}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                            c.SEGMENT_START_KEY: 15 * 60 + 32,
                            c.SEGMENT_END_KEY: 15 * 60 + 38}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 15 * 60 + 56,
                          c.SEGMENT_END_KEY: 16 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 22,
                          c.SEGMENT_END_KEY: 17 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 17 * 60 + 37,
                          c.SEGMENT_END_KEY: 18 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 24 * 60 + 56,
                          c.SEGMENT_END_KEY: 25 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 25 * 60 + 2,
                          c.SEGMENT_END_KEY: 25 * 60 + 26}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                            c.SEGMENT_START_KEY: 25 * 60 + 5,
                            c.SEGMENT_END_KEY: 25 * 60 + 12}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 25 * 60 + 26,
                          c.SEGMENT_END_KEY: 25 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 25 * 60 + 28,
                          c.SEGMENT_END_KEY: 26 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 26 * 60 + 6,
                          c.SEGMENT_END_KEY: 26 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 26 * 60 + 12,
                          c.SEGMENT_END_KEY: 26 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 26 * 60 + 36,
                          c.SEGMENT_END_KEY: 26 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 26 * 60 + 40,
                          c.SEGMENT_END_KEY: 26 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 27 * 60 + 4,
                          c.SEGMENT_END_KEY: 27 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 28 * 60 + 23,
                          c.SEGMENT_END_KEY: 28 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 28 * 60 + 44,
                          c.SEGMENT_END_KEY: 28 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 29 * 60 + 6,
                          c.SEGMENT_END_KEY: 29 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 29 * 60 + 20,
                          c.SEGMENT_END_KEY: 29 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 29 * 60 + 53,
                          c.SEGMENT_END_KEY: 29 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 30 * 60 + 32,
                          c.SEGMENT_END_KEY: 31 * 60 + 8}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                            c.SEGMENT_START_KEY: 30 * 60 + 36,
                            c.SEGMENT_END_KEY: 30 * 60 + 39}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 31 * 60 + 18,
                          c.SEGMENT_END_KEY: 31 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 31 * 60 + 49,
                          c.SEGMENT_END_KEY: 32 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 31 * 60 + 56,
                          c.SEGMENT_END_KEY: 32 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 31 * 60 + 59,
                          c.SEGMENT_END_KEY: 32 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 32 * 60 + 6,
                          c.SEGMENT_END_KEY: 32 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 33 * 60 + 52,
                          c.SEGMENT_END_KEY: 33 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 34 * 60 + 3,
                          c.SEGMENT_END_KEY: 34 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 34 * 60 + 41,
                          c.SEGMENT_END_KEY: 34 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 35 * 60 + 7,
                          c.SEGMENT_END_KEY: 35 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 41 * 60 + 6,
                          c.SEGMENT_END_KEY: 41 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 41 * 60 + 15,
                          c.SEGMENT_END_KEY: 41 * 60 + 44}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                            c.SEGMENT_START_KEY: 41 * 60 + 30,
                            c.SEGMENT_END_KEY: 41 * 60 + 36}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 41 * 60 + 59,
                          c.SEGMENT_END_KEY: 42 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 42 * 60 + 18,
                          c.SEGMENT_END_KEY: 42 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 42 * 60 + 22,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 42 * 60 + 38,
                          c.SEGMENT_END_KEY: 42 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 42 * 60 + 46,
                          c.SEGMENT_END_KEY: 42 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 42 * 60 + 58,
                          c.SEGMENT_END_KEY: 43 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 43 * 60 + 16,
                          c.SEGMENT_END_KEY: 43 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 43 * 60 + 29,
                          c.SEGMENT_END_KEY: 44 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 43 * 60 + 57,
                          c.SEGMENT_END_KEY: 44 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 44 * 60 + 44,
                          c.SEGMENT_END_KEY: 45 * 60 + 17}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                            c.SEGMENT_START_KEY: 44 * 60 + 46,
                            c.SEGMENT_END_KEY: 44 * 60 + 51}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 44 * 60 + 57,
                          c.SEGMENT_END_KEY: 45 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 45 * 60 + 17,
                          c.SEGMENT_END_KEY: 45 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 45 * 60 + 22,
                          c.SEGMENT_END_KEY: 45 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 45 * 60 + 34,
                          c.SEGMENT_END_KEY: 45 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 45 * 60 + 55,
                          c.SEGMENT_END_KEY: 46 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 46 * 60 + 41,
                          c.SEGMENT_END_KEY: 47 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 47 * 60 + 30,
                          c.SEGMENT_END_KEY: 47 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 47 * 60 + 41,
                          c.SEGMENT_END_KEY: 47 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 47 * 60 + 57,
                          c.SEGMENT_END_KEY: 48 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 48 * 60 + 22,
                          c.SEGMENT_END_KEY: 48 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 48 * 60 + 29,
                          c.SEGMENT_END_KEY: 49 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 48 * 60 + 29,
                          c.SEGMENT_END_KEY: 48 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 48 * 60 + 29,
                          c.SEGMENT_END_KEY: 48 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 49 * 60 + 4,
                          c.SEGMENT_END_KEY: 49 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 49 * 60 + 7,
                          c.SEGMENT_END_KEY: 49 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 49 * 60 + 12,
                          c.SEGMENT_END_KEY: 49 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 49 * 60 + 25,
                          c.SEGMENT_END_KEY: 49 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 50 * 60 + 25,
                          c.SEGMENT_END_KEY: 50 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 50 * 60 + 25,
                          c.SEGMENT_END_KEY: 50 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 50 * 60 + 25,
                          c.SEGMENT_END_KEY: 50 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 50 * 60 + 52,
                          c.SEGMENT_END_KEY: 51 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 51 * 60 + 14,
                          c.SEGMENT_END_KEY: 51 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 51 * 60 + 55,
                          c.SEGMENT_END_KEY: 52 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 52 * 60 + 2,
                          c.SEGMENT_END_KEY: 52 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 52 * 60 + 50,
                          c.SEGMENT_END_KEY: 52 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 53 * 60 + 8,
                          c.SEGMENT_END_KEY: 53 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 53 * 60 + 44,
                          c.SEGMENT_END_KEY: 53 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 53 * 60 + 44,
                          c.SEGMENT_END_KEY: 54 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 53 * 60 + 44,
                          c.SEGMENT_END_KEY: 53 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 54 * 60,
                          c.SEGMENT_END_KEY: 54 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 54 * 60 + 32,
                          c.SEGMENT_END_KEY: 54 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 54 * 60 + 47,
                          c.SEGMENT_END_KEY: 55 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 55 * 60 + 23,
                          c.SEGMENT_END_KEY: 55 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 55 * 60 + 26,
                          c.SEGMENT_END_KEY: 55 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 55 * 60 + 26,
                          c.SEGMENT_END_KEY: 55 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 55 * 60 + 26,
                          c.SEGMENT_END_KEY: 55 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 55 * 60 + 46,
                          c.SEGMENT_END_KEY: 55 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Fozzi_Luciano',
                          c.SEGMENT_START_KEY: 55 * 60 + 53,
                          c.SEGMENT_END_KEY: 56 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Garzia_Raffaele',
                          c.SEGMENT_START_KEY: 56 * 60 + 19,
                          c.SEGMENT_END_KEY: 56 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Capra_Piero',
                          c.SEGMENT_START_KEY: 56 * 60 + 27,
                          c.SEGMENT_END_KEY: 56 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 56 * 60 + 47,
                          c.SEGMENT_END_KEY: 56 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Mameli_Giacomo',
                          c.SEGMENT_START_KEY: 56 * 60 + 56,
                          c.SEGMENT_END_KEY: 57 * 60 + 18}
    video_segments.append(video_segment_dict)

    # Add durations for video and caption segments,
    # transform seconds in milliseconds
    tot_video_segment_duration = transform_segments(video_segments)
    tot_caption_segment_duration = transform_segments(caption_segments)

    ann_dict = {
        c.VIDEO_SEGMENTS_KEY: video_segments,
        c.TOT_SEGMENT_DURATION_KEY: tot_video_segment_duration,
        c.CAPTION_SEGMENTS_KEY: caption_segments,
        c.TOT_CAPTION_SEGMENT_DURATION_KEY: tot_caption_segment_duration
    }

    # Create necessary directories and save YAML file
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_YAML_file(file_path, ann_dict)

    return ann_dict


def make_MONITOR072011_annotations(file_path):
    """
    Make annotations for MONITOR072011.mpg video file

    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    """

    audio_segments = []
    caption_segments = []
    video_segments = []
    '''
    Templates

    video_segment_dict = {}
    video_segment_dict[c.ANN_TAG_KEY] = ''
    video_segment_dict[c.SEGMENT_START_KEY] =
    video_segment_dict[c.SEGMENT_END_KEY] =
    video_segments.append(video_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[c.ANN_TAG_KEY] = ''
    audio_segment_dict[c.SEGMENT_START_KEY] =
    audio_segment_dict[c.SEGMENT_END_KEY] =
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[c.ANN_TAG_KEY] = ''
    caption_segment_dict[c.SEGMENT_START_KEY] =
    caption_segment_dict[c.SEGMENT_END_KEY] =
    caption_segments.append(caption_segment_dict)
    '''
    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 32, c.SEGMENT_END_KEY: 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura', c.SEGMENT_START_KEY: 48,
                          c.SEGMENT_END_KEY: 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3 * 60 + 6,
                          c.SEGMENT_END_KEY: 3 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3 * 60 + 35,
                          c.SEGMENT_END_KEY: 5 * 60 + 6}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                            c.SEGMENT_START_KEY: 4 * 60 + 56,
                            c.SEGMENT_END_KEY: 5 * 60 + 4}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 5 * 60 + 20,
                          c.SEGMENT_END_KEY: 5 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 5 * 60 + 35,
                          c.SEGMENT_END_KEY: 5 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 5 * 60 + 58,
                          c.SEGMENT_END_KEY: 7 * 60 + 5}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                            c.SEGMENT_START_KEY: 6 * 60 + 15,
                            c.SEGMENT_END_KEY: 6 * 60 + 24}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 7 * 60 + 1,
                          c.SEGMENT_END_KEY: 7 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 7 * 60 + 1,
                          c.SEGMENT_END_KEY: 7 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 7 * 60 + 1,
                          c.SEGMENT_END_KEY: 7 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 7 * 60 + 1,
                          c.SEGMENT_END_KEY: 7 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 7 * 60 + 5,
                          c.SEGMENT_END_KEY: 7 * 60 + 32}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 7 * 60 + 32,
                          c.SEGMENT_END_KEY: 7 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 7 * 60 + 32,
                          c.SEGMENT_END_KEY: 7 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 7 * 60 + 32,
                          c.SEGMENT_END_KEY: 7 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 7 * 60 + 32,
                          c.SEGMENT_END_KEY: 8 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 7 * 60 + 32,
                          c.SEGMENT_END_KEY: 7 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 7 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 7 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 7 * 60 + 40,
                          c.SEGMENT_END_KEY: 7 * 60 + 49}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 9 * 60 + 5,
                          c.SEGMENT_END_KEY: 9 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 9 * 60 + 5,
                          c.SEGMENT_END_KEY: 9 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 9 * 60 + 5,
                          c.SEGMENT_END_KEY: 9 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 9 * 60 + 22,
                          c.SEGMENT_END_KEY: 9 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 9 * 60 + 24,
                          c.SEGMENT_END_KEY: 9 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 9 * 60 + 27,
                          c.SEGMENT_END_KEY: 9 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 9 * 60 + 40,
                          c.SEGMENT_END_KEY: 9 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 10 * 60 + 4,
                          c.SEGMENT_END_KEY: 10 * 60 + 27}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 10 * 60 + 13,
                          c.SEGMENT_END_KEY: 10 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 10 * 60 + 13,
                          c.SEGMENT_END_KEY: 10 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 10 * 60 + 13,
                          c.SEGMENT_END_KEY: 10 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 10 * 60 + 27,
                          c.SEGMENT_END_KEY: 10 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 10 * 60 + 39,
                          c.SEGMENT_END_KEY: 11 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 11 * 60 + 4,
                          c.SEGMENT_END_KEY: 11 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 11 * 60 + 4,
                          c.SEGMENT_END_KEY: 11 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 11 * 60 + 4,
                          c.SEGMENT_END_KEY: 11 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 11 * 60 + 16,
                          c.SEGMENT_END_KEY: 11 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 11 * 60 + 20,
                          c.SEGMENT_END_KEY: 11 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 11 * 60 + 20,
                          c.SEGMENT_END_KEY: 11 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 11 * 60 + 20,
                          c.SEGMENT_END_KEY: 11 * 60 + 24}
    video_segments.append(video_segment_dict)


    # 5 people at the same time
    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 11 * 60 + 30,
                          c.SEGMENT_END_KEY: 11 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 11 * 60 + 30,
                          c.SEGMENT_END_KEY: 11 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 11 * 60 + 30,
                          c.SEGMENT_END_KEY: 11 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 11 * 60 + 30,
                          c.SEGMENT_END_KEY: 11 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 11 * 60 + 30,
                          c.SEGMENT_END_KEY: 11 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 12 * 60 + 1,
                          c.SEGMENT_END_KEY: 12 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 12 * 60 + 10,
                          c.SEGMENT_END_KEY: 12 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 12 * 60 + 16,
                          c.SEGMENT_END_KEY: 13 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 13 * 60 + 12,
                          c.SEGMENT_END_KEY: 13 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 13 * 60 + 25,
                          c.SEGMENT_END_KEY: 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 13 * 60 + 36,
                          c.SEGMENT_END_KEY: 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 13 * 60 + 36,
                          c.SEGMENT_END_KEY: 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 13 * 60 + 55,
                          c.SEGMENT_END_KEY: 14 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 14 * 60 + 14,
                          c.SEGMENT_END_KEY: 14 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 14 * 60 + 26,
                          c.SEGMENT_END_KEY: 14 * 60 + 41}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                            c.SEGMENT_START_KEY: 14 * 60 + 35,
                            c.SEGMENT_END_KEY: 14 * 60 + 43}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 14 * 60 + 42,
                          c.SEGMENT_END_KEY: 14 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 14 * 60 + 50,
                          c.SEGMENT_END_KEY: 14 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 14 * 60 + 53,
                          c.SEGMENT_END_KEY: 15 * 60 + 6}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 18 * 60 + 53,
                          c.SEGMENT_END_KEY: 19 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 19 * 60 + 48,
                          c.SEGMENT_END_KEY: 19 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 19 * 60 + 55,
                          c.SEGMENT_END_KEY: 19 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 19 * 60 + 57,
                          c.SEGMENT_END_KEY: 21 * 60 + 4}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                            c.SEGMENT_START_KEY: 20 * 60 + 4,
                            c.SEGMENT_END_KEY: 20 * 60 + 20}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 21 * 60 + 9,
                          c.SEGMENT_END_KEY: 21 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 21 * 60 + 23,
                          c.SEGMENT_END_KEY: 21 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 21 * 60 + 31,
                          c.SEGMENT_END_KEY: 21 * 60 + 36}
    video_segments.append(video_segment_dict)

    # 3 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 21 * 60 + 36,
                          c.SEGMENT_END_KEY: 21 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 21 * 60 + 36,
                          c.SEGMENT_END_KEY: 21 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 21 * 60 + 36,
                          c.SEGMENT_END_KEY: 21 * 60 + 38}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 21 * 60 + 38,
                          c.SEGMENT_END_KEY: 22 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 22 * 60 + 6,
                          c.SEGMENT_END_KEY: 22 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 22 * 60 + 9,
                          c.SEGMENT_END_KEY: 22 * 60 + 33}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                            c.SEGMENT_START_KEY: 22 * 60 + 16,
                            c.SEGMENT_END_KEY: 22 * 60 + 30}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 22 * 60 + 33,
                          c.SEGMENT_END_KEY: 22 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 22 * 60 + 41,
                          c.SEGMENT_END_KEY: 22 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 22 * 60 + 41,
                          c.SEGMENT_END_KEY: 22 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 22 * 60 + 43,
                          c.SEGMENT_END_KEY: 23 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 23 * 60 + 17,
                          c.SEGMENT_END_KEY: 23 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 23 * 60 + 24,
                          c.SEGMENT_END_KEY: 24 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 24 * 60 + 18,
                          c.SEGMENT_END_KEY: 24 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 24 * 60 + 21,
                          c.SEGMENT_END_KEY: 24 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 24 * 60 + 48,
                          c.SEGMENT_END_KEY: 25 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 25 * 60 + 27,
                          c.SEGMENT_END_KEY: 25 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 25 * 60 + 33,
                          c.SEGMENT_END_KEY: 25 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 25 * 60 + 51,
                          c.SEGMENT_END_KEY: 25 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 26 * 60 + 2,
                          c.SEGMENT_END_KEY: 26 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 26 * 60 + 18,
                          c.SEGMENT_END_KEY: 26 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 26 * 60 + 26,
                          c.SEGMENT_END_KEY: 26 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 26 * 60 + 31,
                          c.SEGMENT_END_KEY: 27 * 60 + 20}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                            c.SEGMENT_START_KEY: 26 * 60 + 44,
                            c.SEGMENT_END_KEY: 26 * 60 + 54}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 27 * 60 + 35,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 28 * 60 + 6,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 28 * 60 + 6,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 28 * 60 + 6,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 28 * 60 + 6,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 28 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 28 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 29 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 28 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 28 * 60 + 21,
                          c.SEGMENT_END_KEY: 28 * 60 + 26}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                            c.SEGMENT_START_KEY: 28 * 60 + 34,
                            c.SEGMENT_END_KEY: 28 * 60 + 40}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 29 * 60 + 25,
                          c.SEGMENT_END_KEY: 29 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 29 * 60 + 55,
                          c.SEGMENT_END_KEY: 29 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 30 * 60 + 7,
                          c.SEGMENT_END_KEY: 30 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 30 * 60 + 30,
                          c.SEGMENT_END_KEY: 30 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 30 * 60 + 41,
                          c.SEGMENT_END_KEY: 31 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 31 * 60 + 50,
                          c.SEGMENT_END_KEY: 32 * 60 + 7}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 35 * 60 + 38,
                          c.SEGMENT_END_KEY: 35 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 35 * 60 + 55,
                          c.SEGMENT_END_KEY: 35 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 36 * 60,
                          c.SEGMENT_END_KEY: 36 * 60 + 6}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                            c.SEGMENT_START_KEY: 36 * 60 + 18,
                            c.SEGMENT_END_KEY: 40 * 60 + 10}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 36 * 60 + 23,
                          c.SEGMENT_END_KEY: 36 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 36 * 60 + 59,
                          c.SEGMENT_END_KEY: 37 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 37 * 60 + 4,
                          c.SEGMENT_END_KEY: 37 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 37 * 60 + 38,
                          c.SEGMENT_END_KEY: 37 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 37 * 60 + 44,
                          c.SEGMENT_END_KEY: 37 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 37 * 60 + 59,
                          c.SEGMENT_END_KEY: 38 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 38 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 38 * 60 + 19,
                          c.SEGMENT_END_KEY: 38 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 38 * 60 + 19,
                          c.SEGMENT_END_KEY: 38 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 38 * 60 + 23,
                          c.SEGMENT_END_KEY: 38 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 38 * 60 + 25,
                          c.SEGMENT_END_KEY: 38 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 38 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 38 * 60 + 30,
                          c.SEGMENT_END_KEY: 38 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 38 * 60 + 33,
                          c.SEGMENT_END_KEY: 38 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 38 * 60 + 37,
                          c.SEGMENT_END_KEY: 38 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 38 * 60 + 48,
                          c.SEGMENT_END_KEY: 38 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 38 * 60 + 55,
                          c.SEGMENT_END_KEY: 39 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 39 * 60 + 21,
                          c.SEGMENT_END_KEY: 40 * 60 + 23}
    video_segments.append(video_segment_dict)

    # 4 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 40 * 60 + 23,
                          c.SEGMENT_END_KEY: 40 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 40 * 60 + 23,
                          c.SEGMENT_END_KEY: 40 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 40 * 60 + 23,
                          c.SEGMENT_END_KEY: 40 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 40 * 60 + 23,
                          c.SEGMENT_END_KEY: 40 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 40 * 60 + 43,
                          c.SEGMENT_END_KEY: 41 * 60 + 35}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                            c.SEGMENT_START_KEY: 40 * 60 + 56,
                            c.SEGMENT_END_KEY: 41 * 60 + 6}
    caption_segments.append(caption_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 41 * 60 + 16,
                          c.SEGMENT_END_KEY: 41 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 41 * 60 + 16,
                          c.SEGMENT_END_KEY: 41 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 41 * 60 + 16,
                          c.SEGMENT_END_KEY: 41 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 41 * 60 + 16,
                          c.SEGMENT_END_KEY: 41 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 41 * 60 + 43,
                          c.SEGMENT_END_KEY: 42 * 60}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 42 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 42 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 42 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 42 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 42 * 60,
                          c.SEGMENT_END_KEY: 42 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 42 * 60 + 8,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 42 * 60 + 31,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 42 * 60 + 31,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 42 * 60 + 31,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 42 * 60 + 31,
                          c.SEGMENT_END_KEY: 42 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 42 * 60 + 53,
                          c.SEGMENT_END_KEY: 43 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 43 * 60 + 4,
                          c.SEGMENT_END_KEY: 43 * 60 + 6}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 43 * 60 + 6,
                          c.SEGMENT_END_KEY: 43 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 43 * 60 + 6,
                          c.SEGMENT_END_KEY: 43 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 43 * 60 + 6,
                          c.SEGMENT_END_KEY: 43 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 43 * 60 + 6,
                          c.SEGMENT_END_KEY: 43 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 43 * 60 + 6,
                          c.SEGMENT_END_KEY: 43 * 60 + 9}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 43 * 60 + 11,
                          c.SEGMENT_END_KEY: 43 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 43 * 60 + 11,
                          c.SEGMENT_END_KEY: 43 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 43 * 60 + 11,
                          c.SEGMENT_END_KEY: 43 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 43 * 60 + 11,
                          c.SEGMENT_END_KEY: 43 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 43 * 60 + 15,
                          c.SEGMENT_END_KEY: 43 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 43 * 60 + 18,
                          c.SEGMENT_END_KEY: 44 * 60 + 6}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                            c.SEGMENT_START_KEY: 43 * 60 + 31,
                            c.SEGMENT_END_KEY: 43 * 60 + 41}
    caption_segments.append(caption_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 44 * 60 + 6,
                          c.SEGMENT_END_KEY: 44 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 44 * 60 + 13,
                          c.SEGMENT_END_KEY: 44 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 44 * 60 + 21,
                          c.SEGMENT_END_KEY: 44 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 44 * 60 + 25,
                          c.SEGMENT_END_KEY: 44 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 44 * 60 + 37,
                          c.SEGMENT_END_KEY: 44 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 44 * 60 + 53,
                          c.SEGMENT_END_KEY: 45 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 45 * 60 + 14,
                          c.SEGMENT_END_KEY: 45 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 45 * 60 + 44,
                          c.SEGMENT_END_KEY: 46 * 60 + 8}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                            c.SEGMENT_START_KEY: 46 * 60 + 4,
                            c.SEGMENT_END_KEY: 46 * 60 + 7}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 46 * 60 + 9,
                          c.SEGMENT_END_KEY: 46 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 46 * 60 + 14,
                          c.SEGMENT_END_KEY: 46 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 46 * 60 + 31,
                          c.SEGMENT_END_KEY: 46 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 46 * 60 + 41,
                          c.SEGMENT_END_KEY: 46 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 46 * 60 + 41,
                          c.SEGMENT_END_KEY: 46 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 46 * 60 + 45,
                          c.SEGMENT_END_KEY: 46 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 46 * 60 + 48,
                          c.SEGMENT_END_KEY: 46 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 46 * 60 + 52,
                          c.SEGMENT_END_KEY: 46 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 46 * 60 + 56,
                          c.SEGMENT_END_KEY: 47 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 47 * 60 + 3,
                          c.SEGMENT_END_KEY: 47 * 60 + 5}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 50 * 60 + 33,
                          c.SEGMENT_END_KEY: 50 * 60 + 55}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 50 * 60 + 55,
                          c.SEGMENT_END_KEY: 50 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 50 * 60 + 55,
                          c.SEGMENT_END_KEY: 51 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 50 * 60 + 55,
                          c.SEGMENT_END_KEY: 51 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 50 * 60 + 55,
                          c.SEGMENT_END_KEY: 51 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 50 * 60 + 55,
                          c.SEGMENT_END_KEY: 51 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 50 * 60 + 58,
                          c.SEGMENT_END_KEY: 51 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 50 * 60 + 59,
                          c.SEGMENT_END_KEY: 51 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 51 * 60 + 2,
                          c.SEGMENT_END_KEY: 52 * 60 + 2}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                            c.SEGMENT_START_KEY: 51 * 60 + 26,
                            c.SEGMENT_END_KEY: 51 * 60 + 31}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 52 * 60 + 3,
                          c.SEGMENT_END_KEY: 52 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 52 * 60 + 8,
                          c.SEGMENT_END_KEY: 52 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 52 * 60 + 18,
                          c.SEGMENT_END_KEY: 52 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 52 * 60 + 28,
                          c.SEGMENT_END_KEY: 52 * 60 + 50}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                            c.SEGMENT_START_KEY: 52 * 60 + 33,
                            c.SEGMENT_END_KEY: 52 * 60 + 50}
    caption_segments.append(caption_segment_dict)

    # 3 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 52 * 60 + 50,
                          c.SEGMENT_END_KEY: 53 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 52 * 60 + 50,
                          c.SEGMENT_END_KEY: 53 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 52 * 60 + 50,
                          c.SEGMENT_END_KEY: 53 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 53 * 60 + 5,
                          c.SEGMENT_END_KEY: 53 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 53 * 60 + 15,
                          c.SEGMENT_END_KEY: 53 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 53 * 60 + 21,
                          c.SEGMENT_END_KEY: 53 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 53 * 60 + 29,
                          c.SEGMENT_END_KEY: 53 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 53 * 60 + 29,
                          c.SEGMENT_END_KEY: 53 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 53 * 60 + 29,
                          c.SEGMENT_END_KEY: 53 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 53 * 60 + 35,
                          c.SEGMENT_END_KEY: 53 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 53 * 60 + 37,
                          c.SEGMENT_END_KEY: 53 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 53 * 60 + 45,
                          c.SEGMENT_END_KEY: 53 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 53 * 60 + 53,
                          c.SEGMENT_END_KEY: 53 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 53 * 60 + 58,
                          c.SEGMENT_END_KEY: 54 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 54 * 60 + 14,
                          c.SEGMENT_END_KEY: 54 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 54 * 60 + 28,
                          c.SEGMENT_END_KEY: 54 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 54 * 60 + 37,
                          c.SEGMENT_END_KEY: 54 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 55 * 60 + 11,
                          c.SEGMENT_END_KEY: 55 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 55 * 60 + 22,
                          c.SEGMENT_END_KEY: 55 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 55 * 60 + 46,
                          c.SEGMENT_END_KEY: 55 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 55 * 60 + 49,
                          c.SEGMENT_END_KEY: 56 * 60 + 2}
    video_segments.append(video_segment_dict)

    # 3 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 56 * 60 + 2,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 56 * 60 + 2,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 56 * 60 + 2,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 56 * 60 + 6,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 56 * 60 + 8,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 56 * 60 + 9,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 56 * 60 + 10,
                          c.SEGMENT_END_KEY: 56 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 56 * 60 + 11,
                          c.SEGMENT_END_KEY: 56 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 56 * 60 + 14,
                          c.SEGMENT_END_KEY: 56 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 56 * 60 + 39,
                          c.SEGMENT_END_KEY: 57 * 60 + 17}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                            c.SEGMENT_START_KEY: 56 * 60 + 46,
                            c.SEGMENT_END_KEY: 56 * 60 + 54}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 57 * 60 + 21,
                          c.SEGMENT_END_KEY: 57 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 57 * 60 + 25,
                          c.SEGMENT_END_KEY: 57 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 57 * 60 + 42,
                          c.SEGMENT_END_KEY: 57 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 57 * 60 + 57,
                          c.SEGMENT_END_KEY: 58 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 58 * 60 + 15,
                          c.SEGMENT_END_KEY: 1 * 3600 + 4}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                            c.SEGMENT_START_KEY: 58 * 60 + 27,
                            c.SEGMENT_END_KEY: 58 * 60 + 35}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 1 * 3600 + 10,
                          c.SEGMENT_END_KEY: 1 * 3600 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 1 * 3600 + 39,
                          c.SEGMENT_END_KEY: 1 * 3600 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 1 * 3600 + 43,
                          c.SEGMENT_END_KEY: 1 * 3600 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 59,
                          c.SEGMENT_END_KEY: 3600 + 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 59,
                          c.SEGMENT_END_KEY: 3600 + 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 3 * 60,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 5}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 14}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 14}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 14}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                            c.SEGMENT_START_KEY: 3600 + 5 * 60 + 53,
                            c.SEGMENT_END_KEY: 3600 + 8 * 60 + 50}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 22}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 27}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 27}
    video_segments.append(video_segment_dict)

    # 5 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)


    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 23,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 50}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                            c.SEGMENT_START_KEY: 3600 + 8 * 60 + 53,
                            c.SEGMENT_END_KEY: 3600 + 9 * 60 + 16}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 9 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 9 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 9 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 9 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 42}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                            c.SEGMENT_START_KEY: 3600 + 10 * 60 + 57,
                            c.SEGMENT_END_KEY: 3600 + 12 * 60 + 7}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 13}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                            c.SEGMENT_START_KEY: 3600 + 12 * 60 + 40,
                            c.SEGMENT_END_KEY: 3600 + 12 * 60 + 50}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 16,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 45,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 15 * 60 + 6}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 3}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'De_Berardinis_Gianni',
                            c.SEGMENT_START_KEY: 3600 + 20 * 60 + 45,
                            c.SEGMENT_END_KEY: 3600 + 23 * 60 + 8}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 12,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 20,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 25,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 32}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                            c.SEGMENT_START_KEY: 3600 + 24 * 60 + 11,
                            c.SEGMENT_END_KEY: 3600 + 24 * 60 + 24}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 13}
    video_segments.append(video_segment_dict)

    # 4 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                            c.SEGMENT_START_KEY: 3600 + 25 * 60 + 25,
                            c.SEGMENT_END_KEY: 3600 + 25 * 60 + 35}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 45,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 29,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 49}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 32 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 29,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 18}
    video_segments.append(video_segment_dict)

    # 6 persone contemporaneamente

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 40 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 40 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 40 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 40 * 60 + 20,
                          c.SEGMENT_END_KEY: 3600 + 40 * 60 + 43}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Annalisa',
                            c.SEGMENT_START_KEY: 3600 + 40 * 60 + 36,
                            c.SEGMENT_END_KEY: 3600 + 43 * 60 + 18}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 40 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 40 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 40 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 17,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 25,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 29,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 45 * 60}
    video_segments.append(video_segment_dict)

    # Pubblicita'

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 48 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 48 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 48 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 48 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 48 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 48 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 48 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 49 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 49 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 49 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 49 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 49 * 60 + 24}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                            c.SEGMENT_START_KEY: 3600 + 49 * 60 + 16,
                            c.SEGMENT_END_KEY: 3600 + 49 * 60 + 23}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 49 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 50 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 50 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 50 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 50 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 50 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 50 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 50 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 53 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 53 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 53 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 53 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 54 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 54 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 54 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 54 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 55 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 12,
                          c.SEGMENT_END_KEY: 3600 + 55 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 55 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 56 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 9,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 37}
    video_segments.append(video_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3 * 60 + 6,
                          c.SEGMENT_END_KEY: 3 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3 * 60 + 43,
                          c.SEGMENT_END_KEY: 5 * 60 + 37}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 5 * 60 + 38,
                          c.SEGMENT_END_KEY: 5 * 60 + 55}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 5 * 60 + 56,
                          c.SEGMENT_END_KEY: 7 * 60 + 3}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 7 * 60 + 3,
                          c.SEGMENT_END_KEY: 7 * 60 + 45}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 7 * 60 + 46,
                          c.SEGMENT_END_KEY: 8 * 60 + 26}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 8 * 60 + 27,
                          c.SEGMENT_END_KEY: 8 * 60 + 33}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 8 * 60 + 34,
                          c.SEGMENT_END_KEY: 9 * 60 + 20}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 9 * 60 + 20,
                          c.SEGMENT_END_KEY: 9 * 60 + 23}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 9 * 60 + 23,
                          c.SEGMENT_END_KEY: 9 * 60 + 26}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 9 * 60 + 29,
                          c.SEGMENT_END_KEY: 10 * 60 + 24}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 10 * 60 + 27,
                          c.SEGMENT_END_KEY: 10 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 10 * 60 + 39,
                          c.SEGMENT_END_KEY: 10 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 10 * 60 + 59,
                          c.SEGMENT_END_KEY: 11 * 60 + 14}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 11 * 60 + 14,
                          c.SEGMENT_END_KEY: 11 * 60 + 19}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 11 * 60 + 19,
                          c.SEGMENT_END_KEY: 11 * 60 + 23}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 11 * 60 + 25,
                          c.SEGMENT_END_KEY: 12 * 60 + 8}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 12 * 60 + 8,
                          c.SEGMENT_END_KEY: 12 * 60 + 16}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 12 * 60 + 17,
                          c.SEGMENT_END_KEY: 13 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 13 * 60 + 6,
                          c.SEGMENT_END_KEY: 13 * 60 + 19}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 13 * 60 + 19,
                          c.SEGMENT_END_KEY: 13 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 13 * 60 + 22,
                          c.SEGMENT_END_KEY: 13 * 60 + 48}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 13 * 60 + 49,
                          c.SEGMENT_END_KEY: 14 * 60 + 18}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 14 * 60 + 18,
                          c.SEGMENT_END_KEY: 14 * 60 + 39}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 14 * 60 + 40,
                          c.SEGMENT_END_KEY: 15 * 60 + 6}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 18 * 60 + 51,
                          c.SEGMENT_END_KEY: 19 * 60 + 55}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 19 * 60 + 56,
                          c.SEGMENT_END_KEY: 21 * 60 + 18}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 21 * 60 + 20,
                          c.SEGMENT_END_KEY: 21 * 60 + 28}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 21 * 60 + 28,
                          c.SEGMENT_END_KEY: 23 * 60 + 10}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 23 * 60 + 11,
                          c.SEGMENT_END_KEY: 23 * 60 + 19}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 23 * 60 + 20,
                          c.SEGMENT_END_KEY: 25 * 60 + 58}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 25 * 60 + 59,
                          c.SEGMENT_END_KEY: 26 * 60 + 31}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 26 * 60 + 31,
                          c.SEGMENT_END_KEY: 28 * 60 + 10}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 28 * 60 + 11,
                          c.SEGMENT_END_KEY: 28 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 28 * 60 + 16,
                          c.SEGMENT_END_KEY: 30 * 60 + 27}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 30 * 60 + 28,
                          c.SEGMENT_END_KEY: 30 * 60 + 36}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 30 * 60 + 36,
                          c.SEGMENT_END_KEY: 31 * 60 + 48}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 31 * 60 + 48,
                          c.SEGMENT_END_KEY: 32 * 60 + 7}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 35 * 60 + 36,
                          c.SEGMENT_END_KEY: 36 * 60 + 1}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 36 * 60 + 2,
                          c.SEGMENT_END_KEY: 36 * 60 + 37}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 36 * 60 + 38,
                          c.SEGMENT_END_KEY: 36 * 60 + 53}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 36 * 60 + 54,
                          c.SEGMENT_END_KEY: 38 * 60}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 38 * 60 + 1,
                          c.SEGMENT_END_KEY: 38 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 38 * 60 + 15,
                          c.SEGMENT_END_KEY: 39 * 60 + 9}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 39 * 60 + 9,
                          c.SEGMENT_END_KEY: 39 * 60 + 17}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 39 * 60 + 18,
                          c.SEGMENT_END_KEY: 39 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 39 * 60 + 57,
                          c.SEGMENT_END_KEY: 40 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 40 * 60 + 43,
                          c.SEGMENT_END_KEY: 41 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 41 * 60 + 59,
                          c.SEGMENT_END_KEY: 42 * 60 + 3}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pinna_Laura',
                          c.SEGMENT_START_KEY: 42 * 60 + 2,
                          c.SEGMENT_END_KEY: 43 * 60 + 3}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 43 * 60 + 3,
                          c.SEGMENT_END_KEY: 44 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 44 * 60 + 5,
                          c.SEGMENT_END_KEY: 44 * 60 + 11}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Giagnoli_Gerardo',
                          c.SEGMENT_START_KEY: 44 * 60 + 12,
                          c.SEGMENT_END_KEY: 44 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 44 * 60 + 43,
                          c.SEGMENT_END_KEY: 44 * 60 + 58}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 44 * 60 + 59,
                          c.SEGMENT_END_KEY: 46 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 46 * 60 + 5,
                          c.SEGMENT_END_KEY: 46 * 60 + 18}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 46 * 60 + 19,
                          c.SEGMENT_END_KEY: 46 * 60 + 51}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 46 * 60 + 51,
                          c.SEGMENT_END_KEY: 47 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 50 * 60 + 31,
                          c.SEGMENT_END_KEY: 51 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 51 * 60 + 5,
                          c.SEGMENT_END_KEY: 52 * 60 + 1}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 52 * 60 + 1,
                          c.SEGMENT_END_KEY: 52 * 60 + 25}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Vacca_Elias',
                          c.SEGMENT_START_KEY: 52 * 60 + 28,
                          c.SEGMENT_END_KEY: 56 * 60 + 7}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 56 * 60 + 7,
                          c.SEGMENT_END_KEY: 56 * 60 + 38}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 56 * 60 + 40,
                          c.SEGMENT_END_KEY: 57 * 60 + 22}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 57 * 60 + 22,
                          c.SEGMENT_END_KEY: 57 * 60 + 26}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 57 * 60 + 26,
                          c.SEGMENT_END_KEY: 57 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 57 * 60 + 56,
                          c.SEGMENT_END_KEY: 58 * 60 + 18}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sassu_Mario',
                          c.SEGMENT_START_KEY: 58 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 43}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    # Pubblicita'

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 25}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 16,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 21}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 8}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 9,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 49}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 56}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 56,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 40}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 51}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 4}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 6}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Polo_Marinella',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 27}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 54}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 15 * 60 + 5}
    audio_segments.append(audio_segment_dict)

    # Pubblicita'

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 47}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 53}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 57}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 52}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Luisa',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 20}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 38}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'De_Berardinis_Gianni',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 32}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'De_Berardinis_Gianni',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 26}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 46}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Pisano_Francesco',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 47}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 15}
    audio_segments.append(audio_segment_dict)

    # Review fino a 1h 25 minuti

    audio_segment_dict = {c.ANN_TAG_KEY: 'Luciano_Nicola',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 59}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Minutti_Giampaola',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 35}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60 + 41}
    audio_segments.append(audio_segment_dict)

    audio_segment_dict = {c.ANN_TAG_KEY: 'Corona_Giorgia',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 42,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 25}
    audio_segments.append(audio_segment_dict)

    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = 'Dessi_Emanuele'
    # audio_segment_dict[c.SEGMENT_START_KEY] = 3600 + 28*60 + 25
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)
    #
    # audio_segment_dict = {}
    # audio_segment_dict[c.ANN_TAG_KEY] = ''
    # audio_segment_dict[c.SEGMENT_START_KEY] =
    # audio_segment_dict[c.SEGMENT_END_KEY] =
    # audio_segments.append(audio_segment_dict)

    '''
    Templates

    video_segment_dict = {}
    video_segment_dict[c.ANN_TAG_KEY] = ''
    video_segment_dict[c.SEGMENT_START_KEY] = 3600 +
    video_segment_dict[c.SEGMENT_END_KEY] = 3600 +
    video_segments.append(video_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[c.ANN_TAG_KEY] = ''
    audio_segment_dict[c.SEGMENT_START_KEY] =
    audio_segment_dict[c.SEGMENT_END_KEY] =
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[c.ANN_TAG_KEY] = ''
    caption_segment_dict[c.SEGMENT_START_KEY] =
    caption_segment_dict[c.SEGMENT_END_KEY] =
    caption_segments.append(caption_segment_dict)
    '''

    # Add durations for video and caption segments,
    # transform seconds in milliseconds
    tot_video_segment_duration = transform_segments(video_segments)
    tot_caption_segment_duration = transform_segments(caption_segments)

    ann_dict = {
        c.VIDEO_SEGMENTS_KEY: video_segments,
        c.TOT_SEGMENT_DURATION_KEY: tot_video_segment_duration,
        c.CAPTION_SEGMENTS_KEY: caption_segments,
        c.TOT_CAPTION_SEGMENT_DURATION_KEY: tot_caption_segment_duration
    }

    # Create necessary directories and save YAML file
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_YAML_file(file_path, ann_dict)

    return ann_dict


def make_MONITOR272010_annotations(file_path):
    """
    Make annotations for MONITOR272010.mpg video file

    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    """

    caption_segments = []
    video_segments = []
    '''
    Templates

    video_segment_dict = {}
    video_segment_dict[c.ANN_TAG_KEY] = ''
    video_segment_dict[c.SEGMENT_START_KEY] =
    video_segment_dict[c.SEGMENT_END_KEY] =
    video_segments.append(video_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[c.ANN_TAG_KEY] = ''
    audio_segment_dict[c.SEGMENT_START_KEY] =
    audio_segment_dict[c.SEGMENT_END_KEY] =
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[c.ANN_TAG_KEY] = ''
    caption_segment_dict[c.SEGMENT_START_KEY] =
    caption_segment_dict[c.SEGMENT_END_KEY] =
    caption_segments.append(caption_segment_dict)
    '''
    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 60 + 35,
                          c.SEGMENT_END_KEY: 60 + 59}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                            c.SEGMENT_START_KEY: 60 + 48,
                            c.SEGMENT_END_KEY: 60 + 52}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 60 + 59,
                          c.SEGMENT_END_KEY: 2 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 2 * 60 + 3,
                          c.SEGMENT_END_KEY: 2 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 2 * 60 + 8,
                          c.SEGMENT_END_KEY: 2 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 2 * 60 + 11,
                          c.SEGMENT_END_KEY: 2 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 2 * 60 + 14,
                          c.SEGMENT_END_KEY: 2 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 2 * 60 + 17,
                          c.SEGMENT_END_KEY: 2 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 2 * 60 + 22,
                          c.SEGMENT_END_KEY: 2 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 2 * 60 + 24,
                          c.SEGMENT_END_KEY: 2 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 2 * 60 + 28,
                          c.SEGMENT_END_KEY: 2 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 2 * 60 + 55,
                          c.SEGMENT_END_KEY: 2 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sechi_Egidiangela',
                          c.SEGMENT_START_KEY: 2 * 60 + 59,
                          c.SEGMENT_END_KEY: 3 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3 * 60 + 11,
                          c.SEGMENT_END_KEY: 4 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 4 * 60 + 25,
                          c.SEGMENT_END_KEY: 5 * 60 + 14}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                            c.SEGMENT_START_KEY: 4 * 60 + 31,
                            c.SEGMENT_END_KEY: 4 * 60 + 38}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 5 * 60 + 14,
                          c.SEGMENT_END_KEY: 5 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 5 * 60 + 17,
                          c.SEGMENT_END_KEY: 5 * 60 + 52}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 5 * 60 + 24,
                            c.SEGMENT_END_KEY: 5 * 60 + 31}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 5 * 60 + 52,
                          c.SEGMENT_END_KEY: 6 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 6 * 60 + 1,
                          c.SEGMENT_END_KEY: 6 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 6 * 60 + 14,
                          c.SEGMENT_END_KEY: 6 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 6 * 60 + 59,
                          c.SEGMENT_END_KEY: 7 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 7 * 60 + 11,
                          c.SEGMENT_END_KEY: 7 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 7 * 60 + 20,
                          c.SEGMENT_END_KEY: 7 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 7 * 60 + 33,
                          c.SEGMENT_END_KEY: 8 * 60 + 17}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                            c.SEGMENT_START_KEY: 7 * 60 + 37,
                            c.SEGMENT_END_KEY: 7 * 60 + 44}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 8 * 60 + 20,
                          c.SEGMENT_END_KEY: 8 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 8 * 60 + 29,
                          c.SEGMENT_END_KEY: 8 * 60 + 49}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                            c.SEGMENT_START_KEY: 8 * 60 + 35,
                            c.SEGMENT_END_KEY: 8 * 60 + 42}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 8 * 60 + 49,
                          c.SEGMENT_END_KEY: 8 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 8 * 60 + 59,
                          c.SEGMENT_END_KEY: 9 * 60 + 23}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                            c.SEGMENT_START_KEY: 9 * 60 + 3,
                            c.SEGMENT_END_KEY: 9 * 60 + 11}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 9 * 60 + 23,
                          c.SEGMENT_END_KEY: 9 * 60 + 33}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sechi_Egidiangela',
                            c.SEGMENT_START_KEY: 10 * 60,
                            c.SEGMENT_END_KEY: 10 * 60 + 7}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sechi_Egidiangela',
                          c.SEGMENT_START_KEY: 10 * 60 + 51,
                          c.SEGMENT_END_KEY: 10 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 10 * 60 + 54,
                          c.SEGMENT_END_KEY: 11 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 11 * 60 + 6,
                          c.SEGMENT_END_KEY: 11 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 11 * 60 + 36,
                          c.SEGMENT_END_KEY: 11 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 15 * 60 + 18,
                          c.SEGMENT_END_KEY: 15 * 60 + 43}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Scalas_Marco',
                            c.SEGMENT_START_KEY: 15 * 60 + 41,
                            c.SEGMENT_END_KEY: 17 * 60 + 12}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 15 * 60 + 56,
                          c.SEGMENT_END_KEY: 16 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 17 * 60 + 11,
                          c.SEGMENT_END_KEY: 17 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 19 * 60 + 57,
                          c.SEGMENT_END_KEY: 20 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 20 * 60 + 22,
                          c.SEGMENT_END_KEY: 20 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 20 * 60 + 36,
                          c.SEGMENT_END_KEY: 20 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 22 * 60 + 42,
                          c.SEGMENT_END_KEY: 22 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 22 * 60 + 54,
                          c.SEGMENT_END_KEY: 24 * 60 + 39}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                            c.SEGMENT_START_KEY: 23 * 60 + 2,
                            c.SEGMENT_END_KEY: 23 * 60 + 6}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 24 * 60 + 41,
                          c.SEGMENT_END_KEY: 24 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 25 * 60 + 4,
                          c.SEGMENT_END_KEY: 25 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 25 * 60 + 47,
                          c.SEGMENT_END_KEY: 25 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 26 * 60 + 16,
                          c.SEGMENT_END_KEY: 26 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 26 * 60 + 59,
                          c.SEGMENT_END_KEY: 27 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 27 * 60 + 10,
                          c.SEGMENT_END_KEY: 27 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 27 * 60 + 31,
                          c.SEGMENT_END_KEY: 28 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 28 * 60 + 19,
                          c.SEGMENT_END_KEY: 28 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 28 * 60 + 28,
                          c.SEGMENT_END_KEY: 28 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 32 * 60 + 56,
                          c.SEGMENT_END_KEY: 33 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 33 * 60 + 24,
                          c.SEGMENT_END_KEY: 33 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 33 * 60 + 35,
                          c.SEGMENT_END_KEY: 33 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 33 * 60 + 48,
                          c.SEGMENT_END_KEY: 34 * 60 + 9}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 33 * 60 + 55,
                            c.SEGMENT_END_KEY: 34 * 60 + 1}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 34 * 60 + 9,
                          c.SEGMENT_END_KEY: 34 * 60 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 34 * 60 + 16,
                          c.SEGMENT_END_KEY: 34 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 34 * 60 + 22,
                          c.SEGMENT_END_KEY: 34 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 34 * 60 + 25,
                          c.SEGMENT_END_KEY: 34 * 60 + 33}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                            c.SEGMENT_START_KEY: 34 * 60 + 29,
                            c.SEGMENT_END_KEY: 34 * 60 + 33}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 34 * 60 + 33,
                          c.SEGMENT_END_KEY: 34 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 34 * 60 + 38,
                          c.SEGMENT_END_KEY: 34 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 35 * 60 + 2,
                          c.SEGMENT_END_KEY: 35 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 35 * 60 + 30,
                          c.SEGMENT_END_KEY: 35 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 35 * 60 + 50,
                          c.SEGMENT_END_KEY: 36 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 36 * 60 + 13,
                          c.SEGMENT_END_KEY: 36 * 60 + 42}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                            c.SEGMENT_START_KEY: 36 * 60 + 29,
                            c.SEGMENT_END_KEY: 36 * 60 + 36}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 37 * 60 + 56,
                          c.SEGMENT_END_KEY: 38 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 38 * 60 + 34,
                          c.SEGMENT_END_KEY: 38 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 38 * 60 + 56,
                          c.SEGMENT_END_KEY: 38 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 38 * 60 + 59,
                          c.SEGMENT_END_KEY: 39 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 39 * 60 + 19,
                          c.SEGMENT_END_KEY: 39 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 41 * 60 + 31,
                          c.SEGMENT_END_KEY: 41 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 41 * 60 + 51,
                          c.SEGMENT_END_KEY: 42 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 42 * 60 + 2,
                          c.SEGMENT_END_KEY: 42 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 42 * 60 + 7,
                          c.SEGMENT_END_KEY: 42 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 42 * 60 + 53,
                          c.SEGMENT_END_KEY: 42 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 42 * 60 + 59,
                          c.SEGMENT_END_KEY: 43 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 43 * 60 + 11,
                          c.SEGMENT_END_KEY: 43 * 60 + 29}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                            c.SEGMENT_START_KEY: 43 * 60 + 17,
                            c.SEGMENT_END_KEY: 43 * 60 + 23}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 43 * 60 + 33,
                          c.SEGMENT_END_KEY: 43 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 44 * 60 + 3,
                          c.SEGMENT_END_KEY: 44 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 48 * 60 + 48,
                          c.SEGMENT_END_KEY: 49 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 51 * 60,
                          c.SEGMENT_END_KEY: 51 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 51 * 60 + 13,
                          c.SEGMENT_END_KEY: 51 * 60 + 53}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                            c.SEGMENT_START_KEY: 51 * 60 + 37,
                            c.SEGMENT_END_KEY: 51 * 60 + 43}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 52 * 60 + 13,
                          c.SEGMENT_END_KEY: 52 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 52 * 60 + 24,
                          c.SEGMENT_END_KEY: 52 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 52 * 60 + 37,
                          c.SEGMENT_END_KEY: 53 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 53 * 60 + 40,
                          c.SEGMENT_END_KEY: 54 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 54 * 60 + 1,
                          c.SEGMENT_END_KEY: 54 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 55 * 60 + 18,
                          c.SEGMENT_END_KEY: 56 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 56 * 60 + 5,
                          c.SEGMENT_END_KEY: 57 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 57 * 60 + 13,
                          c.SEGMENT_END_KEY: 57 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 57 * 60 + 23,
                          c.SEGMENT_END_KEY: 58 * 60 + 22}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 57 * 60 + 27,
                            c.SEGMENT_END_KEY: 57 * 60 + 33}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 58 * 60 + 39,
                          c.SEGMENT_END_KEY: 59 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 59 * 60 + 2,
                          c.SEGMENT_END_KEY: 59 * 60 + 21}
    video_segments.append(video_segment_dict)

    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Giardina_Giuseppe'
    # video_segment_dict[c.SEGMENT_START_KEY] = 59*60 + 28
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 37 +
    # video_segments.append(video_segment_dict)
    # 
    # caption_segment_dict = {}
    # caption_segment_dict[c.ANN_TAG_KEY] = 'Giardina_Giuseppe'
    # caption_segment_dict[c.SEGMENT_START_KEY] = 59*60 + 42
    # caption_segment_dict[c.SEGMENT_END_KEY] = 59*60 + 47
    # caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 6,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 7}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 3600 + 2 * 60 + 17,
                            c.SEGMENT_END_KEY: 3600 + 2 * 60 + 23}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 3 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 38}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                            c.SEGMENT_START_KEY: 3600 + 3 * 60 + 22,
                            c.SEGMENT_END_KEY: 3600 + 3 * 60 + 30}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 3 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 3600 + 4 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 31}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                            c.SEGMENT_START_KEY: 3600 + 4 * 60 + 19,
                            c.SEGMENT_END_KEY: 3600 + 4 * 60 + 25}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 4 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 4 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 4 * 60 + 44,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 9 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 9 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 10,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 35}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                            c.SEGMENT_START_KEY: 3600 + 10 * 60 + 15,
                            c.SEGMENT_END_KEY: 3600 + 10 * 60 + 20}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 15 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60}
    video_segments.append(video_segment_dict)

    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Meloni_Toto'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 16*60 + 6
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 16*60 + 46
    # video_segments.append(video_segment_dict)
    #
    # caption_segment_dict = {}
    # caption_segment_dict[c.ANN_TAG_KEY] = 'Meloni_Toto'
    # caption_segment_dict[c.SEGMENT_START_KEY] = 3600 + 16*60 + 18
    # caption_segment_dict[c.SEGMENT_END_KEY] = 3600 + 16*60 + 23
    # caption_segments.append(caption_segment_dict)
    #
    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Meloni_Toto'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 17*60 + 24
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 17*60 + 38
    # video_segments.append(video_segment_dict)
    #
    # caption_segment_dict = {}
    # caption_segment_dict[c.ANN_TAG_KEY] = 'Meloni_Toto'
    # caption_segment_dict[c.SEGMENT_START_KEY] = 3600 + 17*60 + 30
    # caption_segment_dict[c.SEGMENT_END_KEY] = 3600 + 17*60 + 35
    # caption_segments.append(caption_segment_dict)
    #
    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Meloni_Toto'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 18*60 + 3
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 18*60 + 11
    # video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 44}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                            c.SEGMENT_START_KEY: 3600 + 18 * 60 + 36,
                            c.SEGMENT_END_KEY: 3600 + 18 * 60 + 42}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 45}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                            c.SEGMENT_START_KEY: 3600 + 20 * 60 + 22,
                            c.SEGMENT_END_KEY: 3600 + 20 * 60 + 29}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 51}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                            c.SEGMENT_START_KEY: 3600 + 21 * 60 + 35,
                            c.SEGMENT_END_KEY: 3600 + 21 * 60 + 45}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 30}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 3600 + 22 * 60 + 11,
                            c.SEGMENT_END_KEY: 3600 + 22 * 60 + 18}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 31}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                            c.SEGMENT_START_KEY: 3600 + 24 * 60 + 9,
                            c.SEGMENT_END_KEY: 3600 + 24 * 60 + 17}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 26 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 26 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 27 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 27 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 29 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 20,
                          c.SEGMENT_END_KEY: 3600 + 29 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 28}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                            c.SEGMENT_START_KEY: 3600 + 39 * 60 + 6,
                            c.SEGMENT_END_KEY: 3600 + 39 * 60 + 13}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 48}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                            c.SEGMENT_START_KEY: 3600 + 39 * 60 + 43,
                            c.SEGMENT_END_KEY: 3600 + 39 * 60 + 47}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 39 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sechi_Egidiangela',
                          c.SEGMENT_START_KEY: 3600 + 39 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 1,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 59}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Murrocu_Maria_Grazia',
                            c.SEGMENT_START_KEY: 3600 + 41 * 60 + 16,
                            c.SEGMENT_END_KEY: 3600 + 41 * 60 + 21}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 2}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                            c.SEGMENT_START_KEY: 3600 + 42 * 60 + 34,
                            c.SEGMENT_END_KEY: 3600 + 42 * 60 + 41}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu_Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 13,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 25,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 48 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 48 * 60 + 26}
    video_segments.append(video_segment_dict)

    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Cappellacci_Ugo'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 48*60 + 36
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 49*60 + 29
    # video_segments.append(video_segment_dict)
    #
    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Cappellacci_Ugo'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 49*60 + 48
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 49*60 + 53
    # video_segments.append(video_segment_dict)
    #
    # video_segment_dict = {}
    # video_segment_dict[c.ANN_TAG_KEY] = 'Cappellacci_Ugo'
    # video_segment_dict[c.SEGMENT_START_KEY] = 3600 + 50*60 + 2
    # video_segment_dict[c.SEGMENT_END_KEY] = 3600 + 50*60 + 10
    # video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ladu Fortunato',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 20,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sechi_Egidiangela',
                          c.SEGMENT_START_KEY: 3600 + 53 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 53 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 54 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 54 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Picciau_Gigi',
                          c.SEGMENT_START_KEY: 3600 + 54 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 54 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Valentina',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 55 * 60 + 9}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Prato_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 55 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessi_Emanuele',
                          c.SEGMENT_START_KEY: 3600 + 55 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 56 * 60}
    video_segments.append(video_segment_dict)

    '''
    Templates

    video_segment_dict = {}
    video_segment_dict[c.ANN_TAG_KEY] = ''
    video_segment_dict[c.SEGMENT_START_KEY] =
    video_segment_dict[c.SEGMENT_END_KEY] =
    video_segments.append(video_segment_dict)

    audio_segment_dict = {}
    audio_segment_dict[c.ANN_TAG_KEY] = ''
    audio_segment_dict[c.SEGMENT_START_KEY] =
    audio_segment_dict[c.SEGMENT_END_KEY] =
    audio_segments.append(audio_segment_dict)

    caption_segment_dict = {}
    caption_segment_dict[c.ANN_TAG_KEY] = ''
    caption_segment_dict[c.SEGMENT_START_KEY] =
    caption_segment_dict[c.SEGMENT_END_KEY] =
    caption_segments.append(caption_segment_dict)
    '''

    # Add durations for video and caption segments,
    # transform seconds in milliseconds
    tot_video_segment_duration = transform_segments(video_segments)
    tot_caption_segment_duration = transform_segments(caption_segments)

    ann_dict = {
        c.VIDEO_SEGMENTS_KEY: video_segments,
        c.TOT_SEGMENT_DURATION_KEY: tot_video_segment_duration,
        c.CAPTION_SEGMENTS_KEY: caption_segments,
        c.TOT_CAPTION_SEGMENT_DURATION_KEY: tot_caption_segment_duration
    }

    # Create necessary directories and save YAML file
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    save_YAML_file(file_path, ann_dict)

    return ann_dict

def make_SPALTI3_230907_annotations(file_path):
    """
    Make annotations for SPALTI3_230907.mpg video file

    :type file_path: string
    :param file_path: path of YAML file that will contain annotations
    """

    caption_segments = []
    video_segments = []

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 60 + 26,
                          c.SEGMENT_END_KEY: 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 60 + 26,
                          c.SEGMENT_END_KEY: 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 60 + 57,
                          c.SEGMENT_END_KEY: 2 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 60 + 57,
                          c.SEGMENT_END_KEY: 2 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 60 + 8,
                          c.SEGMENT_END_KEY: 2 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 60 + 8,
                          c.SEGMENT_END_KEY: 2 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 2 * 60 + 17,
                          c.SEGMENT_END_KEY: 2 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 60 + 28,
                          c.SEGMENT_END_KEY: 2 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 60 + 28,
                          c.SEGMENT_END_KEY: 2 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 2 * 60 + 37,
                          c.SEGMENT_END_KEY: 3 * 60 + 8}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                            c.SEGMENT_START_KEY: 2 * 60 + 50,
                            c.SEGMENT_END_KEY: 3 * 60 + 2}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3 * 60 + 8,
                          c.SEGMENT_END_KEY: 3 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3 * 60 + 8,
                          c.SEGMENT_END_KEY: 3 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 3 * 60 + 20,
                          c.SEGMENT_END_KEY: 3 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3 * 60 + 58,
                          c.SEGMENT_END_KEY: 4 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3 * 60 + 58,
                          c.SEGMENT_END_KEY: 4 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 4 * 60 + 10,
                          c.SEGMENT_END_KEY: 5 * 60 + 8}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                            c.SEGMENT_START_KEY: 4 * 60 + 13,
                            c.SEGMENT_END_KEY: 5 * 60 + 8}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 5 * 60 + 9,
                          c.SEGMENT_END_KEY: 5 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 5 * 60 + 9,
                          c.SEGMENT_END_KEY: 5 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 6 * 60 + 39,
                          c.SEGMENT_END_KEY: 6 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 6 * 60 + 39,
                          c.SEGMENT_END_KEY: 6 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 6 * 60 + 58,
                          c.SEGMENT_END_KEY: 7 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 7 * 60 + 4,
                          c.SEGMENT_END_KEY: 7 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 7 * 60 + 26,
                          c.SEGMENT_END_KEY: 7 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 7 * 60 + 33,
                          c.SEGMENT_END_KEY: 7 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 7 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 7 * 60 + 46,
                          c.SEGMENT_END_KEY: 7 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 7 * 60 + 46,
                          c.SEGMENT_END_KEY: 7 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 8 * 60 + 12,
                          c.SEGMENT_END_KEY: 8 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 8 * 60 + 12,
                          c.SEGMENT_END_KEY: 8 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 8 * 60 + 26,
                          c.SEGMENT_END_KEY: 8 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 8 * 60 + 26,
                          c.SEGMENT_END_KEY: 8 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 8 * 60 + 33,
                          c.SEGMENT_END_KEY: 8 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 9 * 60 + 16,
                          c.SEGMENT_END_KEY: 9 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 9 * 60 + 16,
                          c.SEGMENT_END_KEY: 9 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 9 * 60 + 51,
                          c.SEGMENT_END_KEY: 10 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 9 * 60 + 51,
                          c.SEGMENT_END_KEY: 10 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 10 * 60 + 9,
                          c.SEGMENT_END_KEY: 10 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 10 * 60 + 26,
                          c.SEGMENT_END_KEY: 10 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 10 * 60 + 39,
                          c.SEGMENT_END_KEY: 10 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 10 * 60 + 47,
                          c.SEGMENT_END_KEY: 10 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 10 + 60 + 59,
                          c.SEGMENT_END_KEY: 11 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 11 * 60 + 47,
                          c.SEGMENT_END_KEY: 11 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 11 * 60 + 58,
                          c.SEGMENT_END_KEY: 12 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 11 * 60 + 58,
                          c.SEGMENT_END_KEY: 12 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 12 * 60 + 5,
                          c.SEGMENT_END_KEY: 12 * 60 + 28}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 12 * 60 + 28,
                          c.SEGMENT_END_KEY: 12 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 12 * 60 + 28,
                          c.SEGMENT_END_KEY: 12 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 12 * 60 + 38,
                          c.SEGMENT_END_KEY: 13 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 13 * 60 + 5,
                          c.SEGMENT_END_KEY: 13 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 13 * 60 + 5,
                          c.SEGMENT_END_KEY: 13 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 13 * 60 + 7,
                          c.SEGMENT_END_KEY: 13 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 13 * 60 + 30,
                          c.SEGMENT_END_KEY: 13 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 13 * 60 + 34,
                          c.SEGMENT_END_KEY: 13 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 13 * 60 + 34,
                          c.SEGMENT_END_KEY: 13 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 13 * 60 + 36,
                          c.SEGMENT_END_KEY: 13 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 13 * 60 + 51,
                          c.SEGMENT_END_KEY: 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 13 * 60 + 51,
                          c.SEGMENT_END_KEY: 13 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 14 * 60 + 8,
                          c.SEGMENT_END_KEY: 14 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 14 * 60 + 41,
                          c.SEGMENT_END_KEY: 14 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 14 * 60 + 41,
                          c.SEGMENT_END_KEY: 14 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 15 * 60 + 52,
                          c.SEGMENT_END_KEY: 16 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 15 * 60 + 52,
                          c.SEGMENT_END_KEY: 16 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 16 * 60 + 17,
                          c.SEGMENT_END_KEY: 16 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 16 * 60 + 17,
                          c.SEGMENT_END_KEY: 16 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 16 * 60 + 56,
                          c.SEGMENT_END_KEY: 17 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 16 * 60 + 56,
                          c.SEGMENT_END_KEY: 17 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 17 * 60 + 41,
                          c.SEGMENT_END_KEY: 18 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 18 * 60 + 15,
                          c.SEGMENT_END_KEY: 19 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 21 * 60 + 6,
                          c.SEGMENT_END_KEY: 21 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 21 * 60 + 6,
                          c.SEGMENT_END_KEY: 21 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 22 * 60 + 25,
                          c.SEGMENT_END_KEY: 22 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 22 * 60 + 25,
                          c.SEGMENT_END_KEY: 22 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 22 * 60 + 43,
                          c.SEGMENT_END_KEY: 22 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 22 * 60 + 49,
                          c.SEGMENT_END_KEY: 22 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 22 * 60 + 58,
                          c.SEGMENT_END_KEY: 23 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 23 * 60 + 19,
                          c.SEGMENT_END_KEY: 23 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 23 * 60 + 23,
                          c.SEGMENT_END_KEY: 23 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 23 * 60 + 30,
                          c.SEGMENT_END_KEY: 23 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 23 * 60 + 53,
                          c.SEGMENT_END_KEY: 23 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 23 * 60 + 58,
                          c.SEGMENT_END_KEY: 24 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 24 * 60 + 21,
                          c.SEGMENT_END_KEY: 24 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 25 * 60 + 9,
                          c.SEGMENT_END_KEY: 25 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 25 * 60 + 27,
                          c.SEGMENT_END_KEY: 25 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 25 * 60 + 32,
                          c.SEGMENT_END_KEY: 26 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 26 * 60 + 11,
                          c.SEGMENT_END_KEY: 26 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 26 * 60 + 18,
                          c.SEGMENT_END_KEY: 26 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 26 * 60 + 24,
                          c.SEGMENT_END_KEY: 26 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 26 * 60 + 34,
                          c.SEGMENT_END_KEY: 26 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 26 * 60 + 45,
                          c.SEGMENT_END_KEY: 27 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 27 * 60 + 13,
                          c.SEGMENT_END_KEY: 27 * 60 + 22}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 27 * 60 + 22,
                          c.SEGMENT_END_KEY: 28 * 60 + 18}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 27 * 60 + 24,
                            c.SEGMENT_END_KEY: 28 * 60 + 16}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 29 * 60 + 19,
                          c.SEGMENT_END_KEY: 29 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 30 * 60 + 14,
                          c.SEGMENT_END_KEY: 30 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 30 * 60 + 14,
                          c.SEGMENT_END_KEY: 30 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 30 * 60 + 14,
                          c.SEGMENT_END_KEY: 30 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 30 * 60 + 19,
                          c.SEGMENT_END_KEY: 30 * 60 + 57}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 30 * 60 + 21,
                            c.SEGMENT_END_KEY: 30 * 60 + 53}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 31 * 60 + 4,
                          c.SEGMENT_END_KEY: 31 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 31 * 60 + 50,
                          c.SEGMENT_END_KEY: 31 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 32 * 60 + 20,
                          c.SEGMENT_END_KEY: 32 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 32 * 60 + 20,
                          c.SEGMENT_END_KEY: 32 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 32 * 60 + 47,
                          c.SEGMENT_END_KEY: 32 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 32 * 60 + 47,
                          c.SEGMENT_END_KEY: 32 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 33 * 60 + 3,
                          c.SEGMENT_END_KEY: 33 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 33 * 60 + 8,
                          c.SEGMENT_END_KEY: 33 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 33 * 60 + 8,
                          c.SEGMENT_END_KEY: 33 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 33 * 60 + 19,
                          c.SEGMENT_END_KEY: 33 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 33 * 60 + 32,
                          c.SEGMENT_END_KEY: 33 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 33 * 60 + 32,
                          c.SEGMENT_END_KEY: 33 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 33 * 60 + 55,
                          c.SEGMENT_END_KEY: 33 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 34 * 60 + 1,
                          c.SEGMENT_END_KEY: 34 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 34 * 60 + 43,
                          c.SEGMENT_END_KEY: 34 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 34 * 60 + 43,
                          c.SEGMENT_END_KEY: 34 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 34 * 60 + 48,
                          c.SEGMENT_END_KEY: 34 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 34 * 60 + 53,
                          c.SEGMENT_END_KEY: 35 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 34 * 60 + 53,
                          c.SEGMENT_END_KEY: 35 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 35 * 60 + 40,
                          c.SEGMENT_END_KEY: 35 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 35 * 60 + 52,
                          c.SEGMENT_END_KEY: 35 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 35 * 60 + 56,
                          c.SEGMENT_END_KEY: 36 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 35 * 60 + 56,
                          c.SEGMENT_END_KEY: 36 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 36 * 60 + 39,
                          c.SEGMENT_END_KEY: 36 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 36 * 60 + 39,
                          c.SEGMENT_END_KEY: 36 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 36 * 60 + 45,
                          c.SEGMENT_END_KEY: 36 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 36 * 60 + 52,
                          c.SEGMENT_END_KEY: 36 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 38 * 60 + 6,
                          c.SEGMENT_END_KEY: 38 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 38 * 60 + 16,
                          c.SEGMENT_END_KEY: 38 * 60 + 34}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 38 * 60 + 22,
                            c.SEGMENT_END_KEY: 38 * 60 + 34}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 39 * 60 + 2,
                          c.SEGMENT_END_KEY: 39 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 39 * 60 + 15,
                          c.SEGMENT_END_KEY: 40 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 41 * 60 + 1,
                          c.SEGMENT_END_KEY: 41 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 42 * 60 + 3,
                          c.SEGMENT_END_KEY: 42 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 42 * 60 + 28,
                          c.SEGMENT_END_KEY: 42 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 42 * 60 + 28,
                          c.SEGMENT_END_KEY: 42 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 43 * 60 + 5,
                          c.SEGMENT_END_KEY: 43 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 43 * 60 + 5,
                          c.SEGMENT_END_KEY: 43 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 43 * 60 + 44,
                          c.SEGMENT_END_KEY: 44 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 44 * 60 + 7,
                          c.SEGMENT_END_KEY: 44 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 44 * 60 + 7,
                          c.SEGMENT_END_KEY: 44 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 44 * 60 + 27,
                          c.SEGMENT_END_KEY: 44 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 44 * 60 + 27,
                          c.SEGMENT_END_KEY: 44 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 44 * 60 + 34,
                          c.SEGMENT_END_KEY: 44 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 44 * 60 + 34,
                          c.SEGMENT_END_KEY: 44 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 44 * 60 + 55,
                          c.SEGMENT_END_KEY: 45 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 44 * 60 + 55,
                          c.SEGMENT_END_KEY: 45 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 45 * 60,
                          c.SEGMENT_END_KEY: 45 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 45 * 60 + 9,
                          c.SEGMENT_END_KEY: 45 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 48 * 60 + 34,
                          c.SEGMENT_END_KEY: 48 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 49 * 60 + 46,
                          c.SEGMENT_END_KEY: 49 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 50 * 60 + 1,
                          c.SEGMENT_END_KEY: 50 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 50 * 60 + 16,
                          c.SEGMENT_END_KEY: 50 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 50 * 60 + 38,
                          c.SEGMENT_END_KEY: 50 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 50 * 60 + 42,
                          c.SEGMENT_END_KEY: 50 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 51 * 60 + 6,
                          c.SEGMENT_END_KEY: 51 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 52 * 60 + 3,
                          c.SEGMENT_END_KEY: 53 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 53 * 60 + 15,
                          c.SEGMENT_END_KEY: 53 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 53 * 60 + 15,
                          c.SEGMENT_END_KEY: 53 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 54 * 60 + 22,
                          c.SEGMENT_END_KEY: 54 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 54 * 60 + 22,
                          c.SEGMENT_END_KEY: 54 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 55 * 60 + 14,
                          c.SEGMENT_END_KEY: 55 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 55 * 60 + 14,
                          c.SEGMENT_END_KEY: 55 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 55 * 60 + 21,
                          c.SEGMENT_END_KEY: 55 * 60 + 46}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 55 * 60 + 33,
                            c.SEGMENT_END_KEY: 55 * 60 + 46}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 55 * 60 + 52,
                          c.SEGMENT_END_KEY: 56 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 55 * 60 + 52,
                          c.SEGMENT_END_KEY: 56 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 56 * 60 + 3,
                          c.SEGMENT_END_KEY: 56 * 60 + 59}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 56 * 60 + 13,
                            c.SEGMENT_END_KEY: 56 * 60 + 32}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 57 * 60 + 10,
                          c.SEGMENT_END_KEY: 57 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 57 * 60 + 52,
                          c.SEGMENT_END_KEY: 57 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 57 * 60 + 54,
                          c.SEGMENT_END_KEY: 57 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 57 * 60 + 54,
                          c.SEGMENT_END_KEY: 57 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 57 * 60 + 57,
                          c.SEGMENT_END_KEY: 58 * 60 + 2}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 58 * 60 + 6,
                          c.SEGMENT_END_KEY: 58 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 58 * 60 + 22,
                          c.SEGMENT_END_KEY: 58 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 58 * 60 + 22,
                          c.SEGMENT_END_KEY: 58 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 58 * 60 + 41,
                          c.SEGMENT_END_KEY: 59 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 59 * 60 + 23,
                          c.SEGMENT_END_KEY: 59 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 59 * 60 + 31,
                          c.SEGMENT_END_KEY: 59 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 59 * 60 + 31,
                          c.SEGMENT_END_KEY: 59 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 59 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 13,
                          c.SEGMENT_END_KEY: 3600 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 13,
                          c.SEGMENT_END_KEY: 3600 + 16}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 16,
                          c.SEGMENT_END_KEY: 3600 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 60 + 54}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 3600 + 60 + 43,
                            c.SEGMENT_END_KEY: 3600 + 60 + 53}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 57,
                          c.SEGMENT_END_KEY: 3600 + 2 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 2 * 60 + 59,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 38}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 3 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 3 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 3 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 3600 + 4 * 60 + 40,
                          c.SEGMENT_END_KEY: 3600 + 4 * 60 + 58}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 14,
                          c.SEGMENT_END_KEY: 3600 + 5 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 5 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 6 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 3600 + 6 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 38}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                            c.SEGMENT_START_KEY: 3600 + 6 * 60 + 47,
                            c.SEGMENT_END_KEY: 3600 + 7 * 60 + 14}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 7 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 7 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 8 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 3600 + 8 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 9 * 60 + 42}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 9 * 60 + 45,
                          c.SEGMENT_END_KEY: 3600 + 9 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sanna_Vittorio',
                          c.SEGMENT_START_KEY: 3600 + 9 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 33,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 55}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 10 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 3600 + 10 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 11 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 56,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 11 * 60 + 56,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 46,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 12 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 56,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 12 * 60 + 56,
                          c.SEGMENT_END_KEY: 3600 + 13 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 3600 + 13 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 39}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 14 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 15 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 14 * 60 + 50,
                          c.SEGMENT_END_KEY: 3600 + 15 * 60}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 3600 + 15 * 60,
                          c.SEGMENT_END_KEY: 3600 + 15 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 3600 + 15 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 16 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60 + 26}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 16 * 60 + 28,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 16 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 16 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 16 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 16 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 6}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 22,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 25,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 30,
                          c.SEGMENT_END_KEY: 3600 + 17 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 3600 + 17 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 36,
                          c.SEGMENT_END_KEY: 3600 + 18 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 18 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 19}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 45,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 19 * 60 + 51}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 19 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 29}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 20 * 60 + 47}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 3600 + 20 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 5,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 10}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 16,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 19,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 21 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 21 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 22 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 22 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 23 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Porcella_Pietro',
                          c.SEGMENT_START_KEY: 3600 + 23 * 60 + 45,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 3,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 24 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 24 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 35,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 25 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 25 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 28 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 28 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 29 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 29 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 32,
                          c.SEGMENT_END_KEY: 3600 + 29 * 60 + 55}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 3600 + 29 * 60 + 48,
                            c.SEGMENT_END_KEY: 3600 + 29 * 60 + 54}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 30 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_mara',
                          c.SEGMENT_START_KEY: 3600 + 29 * 60 + 55,
                          c.SEGMENT_END_KEY: 3600 + 30 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 3600 + 31 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 32 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 3600 + 32 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 32 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 26,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 33 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 33 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 2,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 8}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 34 * 60 + 47,
                          c.SEGMENT_END_KEY: 3600 + 34 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 35 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 35 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 21,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 36 * 60 + 37,
                          c.SEGMENT_END_KEY: 3600 + 36 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 11,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 38 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 38 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 15,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 38,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 44}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 49,
                          c.SEGMENT_END_KEY: 3600 + 41 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 41 * 60 + 54,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 39}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: ,
                            c.SEGMENT_START_KEY: 3600 + 41 * 60 + 59,
                            c.SEGMENT_END_KEY: 3600 + 42 * 60 + 39}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 43}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 43,
                          c.SEGMENT_END_KEY: 3600 + 42 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 42 * 60 + 58,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 3}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 20}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 20,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 43 * 60 + 34,
                          c.SEGMENT_END_KEY: 3600 + 43 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 17,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 17,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 41,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 52}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Murgia_Alberto',
                          c.SEGMENT_START_KEY: 3600 + 44 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 44 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 45 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 45 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 45 * 60 + 8,
                          c.SEGMENT_END_KEY: 3600 + 45 * 60 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 46 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 46 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 46 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 46 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 50 * 60 + 52,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 30}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                            c.SEGMENT_START_KEY: 3600 + 51 * 60 + 1,
                            c.SEGMENT_END_KEY: 3600 + 51 * 60 + 28}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 51 * 60 + 39,
                          c.SEGMENT_END_KEY: 3600 + 51 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 9,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 13}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 25,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 30}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 31,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 48}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 52 * 60 + 48,
                          c.SEGMENT_END_KEY: 3600 + 52 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 53 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 54 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 53 * 60 + 4,
                          c.SEGMENT_END_KEY: 3600 + 53 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 3600 + 54 * 60 + 51,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 53}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 57 * 60 + 53,
                          c.SEGMENT_END_KEY: 3600 + 57 * 60 + 59}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 7,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 24,
                          c.SEGMENT_END_KEY: 3600 + 58 * 60 + 27}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 3600 + 58 * 60 + 27,
                          c.SEGMENT_END_KEY: 3600 + 59 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Ganau_Gianfranco',
                          c.SEGMENT_START_KEY: 3600 + 59 * 60 + 1,
                          c.SEGMENT_END_KEY: 2 * 3600 + 21}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 22,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 22,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 60 + 27,
                          c.SEGMENT_END_KEY: 2 * 3600 + 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 60 + 27,
                          c.SEGMENT_END_KEY: 2 * 3600 + 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 3 * 60 + 4,
                          c.SEGMENT_END_KEY: 2 * 3600 + 3 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 3 * 60 + 4,
                          c.SEGMENT_END_KEY: 2 * 3600 + 3 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 2 * 3600 + 8 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 7 * 60 + 38,
                          c.SEGMENT_END_KEY: 2 * 3600 + 8 * 60 + 18}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 9 * 60 + 15,
                          c.SEGMENT_END_KEY: 2 * 3600 + 10 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 9 * 60 + 15,
                          c.SEGMENT_END_KEY: 2 * 3600 + 10 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 2 * 3600 + 10 * 60 + 7,
                          c.SEGMENT_END_KEY: 2 * 3600 + 10 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 2 * 3600 + 10 * 60 + 29,
                          c.SEGMENT_END_KEY: 2 * 3600 + 10 * 60 + 35}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 10 * 60 + 52,
                          c.SEGMENT_END_KEY: 2 * 3600 + 11 * 60 + 12}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 11 * 60 + 18,
                          c.SEGMENT_END_KEY: 2 * 3600 + 11 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 11 * 60 + 44,
                          c.SEGMENT_END_KEY: 2 * 3600 + 11 * 60 + 46}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 11 * 60 + 46,
                          c.SEGMENT_END_KEY: 2 * 3600 + 11 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 2 * 3600 + 11 * 60 + 46,
                          c.SEGMENT_END_KEY: 2 * 3600 + 11 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 11 * 60 + 55,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 1}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 1,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 1,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 7}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 7,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 27,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 33,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 33,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 36}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 36,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 40}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 42,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 42,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Dessalvi_Antonello',
                          c.SEGMENT_START_KEY: 2 * 3600 + 12 * 60 + 50,
                          c.SEGMENT_END_KEY: 2 * 3600 + 12 * 60 + 54}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 2 * 3600 + 14 * 60 + 7,
                          c.SEGMENT_END_KEY: 2 * 3600 + 14 * 60 + 17}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 2 * 3600 + 15 * 60 + 50,
                          c.SEGMENT_END_KEY: 2 * 3600 + 15 * 60 + 56}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 16 * 60 + 34,
                          c.SEGMENT_END_KEY: 2 * 3600 + 17 * 60 + 11}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bertola_Sergio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 17 * 60 + 20,
                          c.SEGMENT_END_KEY: 2 * 3600 + 17 * 60 + 33}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Sias_Maria',
                          c.SEGMENT_START_KEY: 2 * 3600 + 17 * 60 + 34,
                          c.SEGMENT_END_KEY: 2 * 3600 + 18 * 60 + 14}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 18 * 60 + 27,
                          c.SEGMENT_END_KEY: 2 * 3600 + 18 * 60 + 50}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 18 * 60 + 59,
                          c.SEGMENT_END_KEY: 2 * 3600 + 19 * 60 + 5}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 19 * 60 + 12,
                          c.SEGMENT_END_KEY: 2 * 3600 + 19 * 60 + 31}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 2 * 3600 + 19 * 60 + 34,
                          c.SEGMENT_END_KEY: 2 * 3600 + 19 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 19 * 60 + 34,
                          c.SEGMENT_END_KEY: 2 * 3600 + 19 * 60 + 57}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Contini_Andrea',
                          c.SEGMENT_START_KEY: 2 * 3600 + 20 * 60 + 6,
                          c.SEGMENT_END_KEY: 2 * 3600 + 20 * 60 + 32}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Uda_Alfio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 20 * 60 + 6,
                          c.SEGMENT_END_KEY: 2 * 3600 + 20 * 60 + 24}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Foschi_Luciano',
                          c.SEGMENT_START_KEY: 2 * 3600 + 20 * 60 + 43,
                          c.SEGMENT_END_KEY: 2 * 3600 + 22 * 60 + 37}
    video_segments.append(video_segment_dict)

    caption_segment_dict = {c.ANN_TAG_KEY: 'Foschi_Luciano',
                            c.SEGMENT_START_KEY: 2 * 3600 + 21 * 60 + 23,
                            c.SEGMENT_END_KEY: 2 * 3600 + 21 * 60 + 29}
    caption_segments.append(caption_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 2 * 3600 + 22 * 60 + 37,
                          c.SEGMENT_END_KEY: 2 * 3600 + 24 * 60 + 34}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 2 * 3600 + 24 * 60 + 58,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25 * 60 + 4}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Foschi_Luciano',
                          c.SEGMENT_START_KEY: 2 * 3600 + 25 * 60 + 4,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25 * 60 + 23}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Foschi_Luciano',
                          c.SEGMENT_START_KEY: 2 * 3600 + 25 * 60 + 26,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25 * 60 + 37}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Argiolas_Ignazio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 25 * 60 + 37,
                          c.SEGMENT_END_KEY: 2 * 3600 + 25 * 60 + 45}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Foschi_Luciano',
                          c.SEGMENT_START_KEY: 2 * 3600 + 25 * 60 + 50,
                          c.SEGMENT_END_KEY: 2 * 3600 + 26 * 60 + 49}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Vargiu_Valerio',
                          c.SEGMENT_START_KEY: 2 * 3600 + 26 * 60 + 49,
                          c.SEGMENT_END_KEY: 2 * 3600 + 27 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Chessa_Mara',
                          c.SEGMENT_START_KEY: 2 * 3600 + 26 * 60 + 49,
                          c.SEGMENT_END_KEY: 2 * 3600 + 27 * 60 + 15}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Bruni_Matteo',
                          c.SEGMENT_START_KEY: 2 * 3600 + 29 * 60 + 32,
                          c.SEGMENT_END_KEY: 2 * 3600 + 29 * 60 + 41}
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: 'Baldaccini_Veronica',
                          c.SEGMENT_START_KEY: 2 * 3600 + 29 * 60 + 41,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)

    video_segment_dict = {c.ANN_TAG_KEY: '',
                          c.SEGMENT_START_KEY: 2 * 3600 +  * 60 + ,
                          c.SEGMENT_END_KEY: 2 * 3600 +  * 60 + }
    video_segments.append(video_segment_dict)


def calculate_stats(ann_dict):
    """
    Calculate statistics for tags in dictionary with annotations

    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video
    """
    tags = get_tags(ann_dict)

    tags_list = []
    for tag in sorted(tags):

        tag_dict = {c.ANN_TAG_KEY: tag}
        person_dict = get_video_annotations_for_person(ann_dict, tag)
        dur = person_dict[c.SEGMENT_DURATION_KEY]
        tag_dict[c.SEGMENT_DURATION_KEY] = dur
        segments_nr = person_dict[c.SEGMENTS_NR_KEY]
        tag_dict[c.SEGMENTS_NR_KEY] = segments_nr
        tags_list.append(tag_dict)

        print(tag_dict)


def get_tags(ann_dict):
    """
    Get list of tags in dictionary with annotations

    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video

    """

    tags = []
    video_segments = ann_dict[c.VIDEO_SEGMENTS_KEY]

    for i in range(0, len(video_segments)):

        ann_tag = video_segments[i][c.ANN_TAG_KEY]

        if not(ann_tag in tags):

            tags.append(ann_tag)

    return tags


def get_video_annotations_for_person(ann_dict, person_tag):
    """
    Get video annotations for given person

    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video

    :type person_tag: string
    :param person_tag: tag of person
    """

    person_dict = {c.ANN_TAG_KEY: person_tag}

    # Save video segments

    person_video_segments = []

    video_segments = ann_dict[c.VIDEO_SEGMENTS_KEY]

    tot_duration = 0

    for video_segment in video_segments:

        ann_tag = video_segment[c.ANN_TAG_KEY]

        # Tag cannot be empty!
        if len(ann_tag) == 0:
            return None

        if ann_tag == person_tag:

            new_person_segment = {}

            start = video_segment[c.SEGMENT_START_KEY]

            new_person_segment[c.SEGMENT_START_KEY] = start

            duration = video_segment[c.SEGMENT_DURATION_KEY]

            # Time cannot be negative!
            if duration < 0:
                print('Warning! Negative duration')
                return None

            tot_duration = tot_duration + duration

            new_person_segment[c.SEGMENT_DURATION_KEY] = duration

            person_video_segments.append(new_person_segment)

    person_dict[c.SEGMENTS_KEY] = person_video_segments

    person_dict[c.SEGMENTS_NR_KEY] = len(person_video_segments)

    person_dict[c.TOT_SEGMENT_DURATION_KEY] = tot_duration

    # Save caption segments

    person_cap_segments = []

    cap_segments = ann_dict[c.CAPTION_SEGMENTS_KEY]

    tot_duration = 0

    for cap_segment in cap_segments:

        ann_tag = cap_segment[c.ANN_TAG_KEY]

        # Tag cannot be empty!
        if len(ann_tag) == 0:
            return None

        if ann_tag == person_tag:

            new_person_segment = {}

            start = cap_segment[c.SEGMENT_START_KEY]

            new_person_segment[c.SEGMENT_START_KEY] = start

            duration = cap_segment[c.SEGMENT_DURATION_KEY]

            # Time cannot be negative!
            if duration < 0:
                print('Warning! Negative duration')
                return None

            tot_duration = tot_duration + duration

            new_person_segment[c.SEGMENT_DURATION_KEY] = duration

            person_cap_segments.append(new_person_segment)

    person_dict[c.CAPTION_SEGMENTS_KEY] = person_cap_segments

    person_dict[c.CAPTION_SEGMENTS_NR_KEY] = len(person_cap_segments)

    person_dict[c.TOT_CAPTION_SEGMENT_DURATION_KEY] = tot_duration

    return person_dict


def save_people_files(ann_dict, video_ann_file_path):
    """
    Save files with the annotations for each people

    :type ann_dict: dictionary
    :param ann_dict: annotations for a whole video

    :video_ann_file_path: string
    :video_ann_file_path: path of file with annotations for whole video
    """

    tags = get_tags(ann_dict)
    print(tags)

    if not os.path.exists(video_ann_file_path):
        os.makedirs(video_ann_file_path)

    for tag in tags:

        person_dict = get_video_annotations_for_person(ann_dict, tag)

        # All people must be correctly annotated
        if person_dict is None:
            return None

        file_name = tag + '.YAML'

        file_path = os.path.join(video_ann_file_path, file_name)

        save_YAML_file(file_path, person_dict)


# video_dir = os.path.join(VIDEO_ANN_PATH, 'MONITOR072011')
#
# file_path_no_ext = os.path.join(video_dir, 'MONITOR072011.mp4')
#
# file_path = file_path_no_ext + '.YAML'
#
# ann_dict = make_MONITOR072011_annotations(file_path)
#
# save_people_files(ann_dict, video_dir)
#
# file_path = r'C:\Users\Maurizio\Documents\Dataset\Videolina-15V\Annotations\MONITOR072011.YAML'
#
# ann_dict = make_MONITOR072011_annotations(file_path)
#
# calculate_stats(ann_dict)

# # fic.02.mpg
# file_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\fic.02.yml'
#
# ann_dir_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\fic.02\Simple annotations'
#
# ann_dict = make_fic02_annotations(file_path)
#
# save_people_files(ann_dict, ann_dir_path)

# Fic.03.mpg
file_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\Fic.03\Fic.03.yml'

ann_dir_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\Fic.03\Simple annotations'

ann_dict =  make_fic03_annotations(file_path)

save_people_files(ann_dict, ann_dir_path)

# # MONITOR072011.mpg
# file_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\MONITOR072011\MONITOR072011.yml'
#
# ann_dir_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\MONITOR072011\Simple annotations'
#
# ann_dict = make_MONITOR072011_annotations(file_path)
#
# save_people_files(ann_dict, ann_dir_path)
#
# # MONITOR272010.mpg
# file_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\MONITOR272010\MONITOR272010.yml'
#
# ann_dir_path = r'C:\Users\Maurizio\Documents\Dataset\Annotazioni\Videolina-15V\MONITOR272010\Simple annotations'
#
# ann_dict = make_MONITOR272010_annotations(file_path)
#
# save_people_files(ann_dict, ann_dir_path)


