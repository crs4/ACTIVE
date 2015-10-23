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
import pickle
from voiceid.sr import Cluster
if __name__ == '__main__':
    pkl_path="/Users/labcontenuti/Music/facciamo_i_conti_internet.wav.pkl"
    cluster  = pickle.load( open( pkl_path, "rb" ) )
    print cluster
    for k in cluster.keys():
        print k, " duration=", cluster[k].get_duration(), " best five=", cluster[k].get_best_five()
        print "."
        