import os
import sys

path_to_be_appended = ".." + os.sep + ".." + os.sep + ".."
sys.path.append(path_to_be_appended)

from tools.face_summarizer import FaceSummarizer

fs = FaceSummarizer()

resource = r'C:\Active\RawVideos\videolina-10sec.mov'

fs.getFrameList(resource)
