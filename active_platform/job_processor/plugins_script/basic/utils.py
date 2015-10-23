# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module is used to define a template for the creation of new Plugin modules.
Some sample scripts signature has been provided and they can be edited in order
to implement new functionalities.

Different functions are imported from the commons module in order to provide
a starting point for script definition.
"""

from plugins_script.commons.utils import get_media_root
from plugins_script.commons.item import set_values
import subprocess
import os
import shutil


def first_script(auth_params, func_params):
    """
    This function is used to print the parameters provided to the script when
    it is invoked by the Job Processor.

    @param auth_params: Authentication parameters provided to this script when it is invoked
    @param func_params: Function parameters provided to the script when it is invoked 
    """
    print auth_params
    print func_params

def second_script(auth_params, func_params):
    """
    This function is used to raise an exception that will be reported in the Job
    that encapsulates the script execution by the job Processor.
    The error message will be visible when the result is retrieved.  

    @param auth_params: Authentication parameters provided to this script when it is invoked
    @param func_params: Function parameters provided to the script when it is invoked 
    """

    raise Exception("Sample exception raised without reason")
