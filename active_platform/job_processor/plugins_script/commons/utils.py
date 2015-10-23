# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module contains all implementative details and system parameter that can be used by
the plugin scripts to execute their tasks.
It has been defined in order to hide all these implementation dependant parameters.
"""

from django.conf import settings


def get_media_root():
    """
    Function used to return the base dir where all items are stored.
    """
    return settings.MEDIA_ROOT


def get_base_dir():
    """
    Function used to return the base dir of the project.
    """
    return settings.BASE_DIR

