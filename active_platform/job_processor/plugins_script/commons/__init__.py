# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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



