# All Rights Reserved. Use is subject to license terms. 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#!/usr/bin/env python

import subprocess
import re
import math
from optparse import OptionParser


length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
re_length = re.compile(length_regexp)
class Split(object):
    def __init__(self, filename, split_length):
        self._filename=filename
        self._split_length=split_length
        
    def ffmpeg_split(self):
    
        #(filename, split_length) = parse_options()
        if self._split_length <= 0:
            print "Split length can't be 0"
            raise SystemExit
    
        output = subprocess.Popen("ffmpeg -i '"+self._filename+"' 2>&1 | grep 'Duration'", 
                                shell = True,
                                stdout = subprocess.PIPE
                                ).stdout.read()
        print output
        matches = re_length.search(output)
        if matches:
            video_length = int(matches.group(1)) * 3600 + \
                            int(matches.group(2)) * 60 + \
                            int(matches.group(3))
            print "Video length in seconds: "+str(video_length)
        else:
            print "Can't determine video length."
            raise SystemExit
    
        split_count = int(math.ceil(video_length/float(self._split_length)))
        if(split_count == 1):
            print "Video length is less then the target split length."
            raise SystemExit
    
        split_cmd = "ffmpeg -i '"+self._filename+"' -vcodec copy -acodec copy"
        #Make output directory
        file_list=[]
        for n in range(0, split_count):
            split_str = ""
            if n == 0:
                split_start = 0
            else:
                split_start = self._split_length * n
            
            split_str += " -ss "+str(split_start)+" -t "+str(self._split_length) + \
                        " '"+self._filename[:-4] + "-" + str(n) + "." + self._filename[-3:] + \
                        "'"
            file_list.append(self._filename[:-4] + "-" + str(n) + "." + self._filename[-3:])
            print "About to run: "+split_cmd+split_str
            output = subprocess.Popen(split_cmd+split_str, shell = True, stdout =
                                   subprocess.PIPE).stdout.read()
        return file_list
    """
    def parse_options(self):
        parser = OptionParser()    
        
        parser.add_option("-f", "--file",
                            dest = "filename",
                            help = "file to split, for example sample.avi",
                            type = "string",
                            action = "store"
                            )
        parser.add_option("-s", "--split-size",
                            dest = "split_size",
                            help = "split or chunk size in seconds, for example 10",
                            type = "int",
                            action = "store"
                            )
        (options, args) = parser.parse_args()
        
        if options.filename and options.split_size:
    
            return (options.filename, options.split_size)
    
        else:
            parser.print_help()
            raise SystemExit
    """
if __name__ == '__main__':

    try: 
        parser = OptionParser()    
        
        parser.add_option("-f", "--file",
                            dest = "filename",
                            help = "file to split, for example sample.avi",
                            type = "string",
                            action = "store"
                            )
        parser.add_option("-s", "--split-size",
                            dest = "split_size",
                            help = "split or chunk size in seconds, for example 10",
                            type = "int",
                            action = "store"
                            )
        (options, args) = parser.parse_args()
        
        if options.filename and options.split_size:    
            s=Split(options.filename,options.split_size )
            print s.ffmpeg_split()
            
        else:
            parser.print_help()
            s=Split("../audio_test/TalkRadio1.wav",20)
            print s.ffmpeg_split()
            
    except Exception, e:
        print "Exception occured running main():"
        print str(e)
    
