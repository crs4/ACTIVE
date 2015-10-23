# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.




"""
This module is used to test the feature extraction framework, using some
digital items to test the correct feature extraction.
The following items has been used to test the functions:
/var/spool/active/data/test/test_image.jpg
/var/spool/active/data/test/test_audio.wav
/var/spool/active/data/test/test_video.vlc
"""

from django.test import TestCase
from plugins_script.feature_extractor.utils import extract_audio_data
from plugins_script.feature_extractor.utils import extract_image_data
from plugins_script.feature_extractor.utils import extract_video_data
from plugins_script.feature_extractor.utils import get_exif_metadata
import subprocess
import os


class TestExifTool(TestCase):
    """
    This class has been defined in order to check
    if the command exiftool has been installed correctely.
    """
    
    def test_cmd(self):
        """
        Check if the command has been installed.
        """
        res = subprocess.call('exiftool', shell=False)
        self.assertEqual(0, res)
    
    def test_audio_metadata(self):
        """
        Check if the command extract all audio item features.
        """
        try:
            audio_path = '/var/spool/active/data/tests/test_audio.wav'
            metadata = get_exif_metadata(audio_path)
            print metadata
            self.assertEqual(True, True)
        except Exception as e:
            self.assertTrue(False)
    
    def test_image_metadata(self):
        """
        Check if the command extract all image item features.
        """
        try:
            image_path = '/var/spool/active/data/tests/test_image.jpg'
            metadata = get_exif_metadata(image_path)
            print metadata
            self.assertEqual(True, True)
        except Exception as e:
            self.assertTrue(False)
    
    def test_video_metadata(self):
        """
        Check if the command extract all video item features.
        """
        try:
            video_path = '/var/spool/active/data/tests/test_video.flv'
            metadata = get_exif_metadata(video_path)
            print metadata
            self.assertEqual(True, True)
        except Exception as e:
            self.assertTrue(False)
