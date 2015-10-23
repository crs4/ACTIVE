# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This module has been created as a simple wrapper for ACTIVE tool objects.
This will be used just for authentication/authorization purposes in the view functions.
"""

from django.db import models

class ActiveTools(models.Model):
    name = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = "ACTIVE Tools"