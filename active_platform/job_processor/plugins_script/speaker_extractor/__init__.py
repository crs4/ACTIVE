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
import os
import glob


#detect all plugins' folders
plugin_folders = [dirs_name for dirs_name in os.listdir(os.path.dirname(__file__)) if os.path.isdir(os.path.join(os.path.dirname(__file__), dirs_name))]

#retrieves all plugin module path from the folders
plugin_modules = []
for f in plugin_folders:
	files = [(os.path.join(f,files_name)) for files_name in os.listdir(os.path.join(os.path.dirname(__file__), f)) if os.path.isfile(os.path.join(os.path.join(os.path.dirname(__file__), f),files_name))]	
	for fi in files:
		temp = fi.split(".")
		if(temp[1] == "py"):
		    plugin_modules.append(temp[0])

#all .py modules in plugins folders are compiled
__all__ = plugin_modules



