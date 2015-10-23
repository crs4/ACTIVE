#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

###################################################################################
# This script must be used in order to install a packaged plug-in in the
# ACTIVE platform. Starting from a compressed archive, it is uncompressed,
# and the files can be moved in the correct directories.
# The path to the ACTIVE plug-in must be provided as script parameter.
# Then it will be uncompressed, unarchived and installed in the platform.
# The plugin is not installed if already existing (manifest or module).
###################################################################################

echo "Installing the ACTIVE plug-in" $1 "..."

# check if the plug-in path exists
if ! [ -e $1 ]; then
    echo "ERROR: ACTIVE plug-in doesn't exist"
    exit 1
fi


# extract plugin name and check if it is already installed
name=`echo "$1" | rev | cut -d"/" -f1 | rev | cut -d"." -f1`
manifest_name=`echo "./"$name".ini"`
module_name=`echo "./"$name"/"`
manifest_dir=`echo "./active_system/plugin_manifest/"`
module_dir=`echo "./job_processor/plugins_script/"`


if [ -e `echo $manifest_dir$manifest_name` ]; then
    echo "ERROR: ACTIVE plug-in manifest already installed"
    exit 1
fi

if [ -d `echo $module_dir$module_name` ]; then
    echo "ERROR: ACTIVE plug-in module already installed"
    exit 1
fi

# uncompress the archive and move files in directories
sudo tar -xvkf $1 
sudo mv $manifest_name $manifest_dir
sudo mv $module_name $module_dir

# remove files in case of error
#sudo rm -rf $manifest_name $manifest_module


echo "ACTIVE plug-in successfully installed."
echo "Restart the ACTIVE platform to detect changes."
