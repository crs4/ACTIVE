# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to test the preview generation plugin, using some
digital items to test the correct preview generation.
The following items has been used to test the functions:
/var/spool/active/data/test/test_image.jpg
/var/spool/active/data/test/test_audio.wav
/var/spool/active/data/test/test_video.vlc
"""

from django.test import TestCase
from plugins_script.adaptation_plugin.utils import _extract_audio_preview
from plugins_script.adaptation_plugin.utils import _extract_image_preview
from plugins_script.adaptation_plugin.utils import _extract_video_preview
import subprocess
import os
import uuid


class TestExifTool(TestCase):
    """
    This class has been defined in order to check
    if the command ffmpeg has been installed correctely.
    """
    
    def test_cmd(self):
        """
        Check if the command has been installed.
        """
        res = subprocess.call(['/usr/bin/ffmpeg', '-h'])
        self.assertEqual(0, res)
    
    def test_cmd2(self):
        """
        Check if the command has been installed.
        """
        res = subprocess.call(['ffmpeg', '-h'])
        self.assertEqual(0, res)
    
    def test_audio_preview(self):
        """
        Check if the command extract all audio item features.
        """
        try:
            audio_path   = '/var/spool/active/data/tests/test_audio.wav'
            preview_path = '/tmp/' + str(uuid.uuid4()) + '.mp3'
            # extract the preview for the audio item
            _extract_audio_preview(audio_path, preview_path)
            # remove the generated preview (if any)
            os.remove(preview_path)
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
    
    def test_image_preview(self):
        """
        Check if the command extract all image item features.
        """
        try:
            image_path = '/var/spool/active/data/tests/test_image.jpg'
            preview_path = '/tmp/' + str(uuid.uuid4()) + '.jpg'
            # extract the preview for the image item
            _extract_image_preview(image_path, preview_path)
            # remove the generated preview (if any)
            os.remove(preview_path)
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
    
    def test_video_preview(self):
        """
        Check if the command extract all video item features.
        """
        try:
            video_path = '/var/spool/active/data/tests/test_video.flv'
            preview_path = '/tmp/' + str(uuid.uuid4()) + '.mp4'
            # extract the preview for the image item
            _extract_video_preview(video_path, preview_path)
            # remove the generated preview (if any)
            os.remove(preview_path)
            self.assertTrue(True)
        except Exception as e:
            print e
            self.assertTrue(False)
