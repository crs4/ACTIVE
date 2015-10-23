# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module used to define a custom middleware necessary to handle the authentication token.
The AuthenticationToken has been defined to handle the request of multimedia files like
thumbnail, previews and original version of resources.
"""

from django.http import HttpRequest, HttpResponse


class TokenAuthentication():
    """
    Class used to retrieve the token from the request and
    save it as header parameter.
    If no token has been defined the HTTP request processing continue.
    """

    def process_request(self, request):
        """
        Retrieve the token parameter from the URL in case of HTTP GET requests.

        @param request: HttpRequest containing the authentication token.
        @type request: HttpRequest
        @return: None
        @rtype: None
        """
	if not request.META.get('HTTP_AUTHORIZATION', None):
            token = request.COOKIES.get('ciccio','123')
	    request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + token

        # continue the processing of this request
        return None
