from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, is_password_usable
#from django.contrib.auth.decorators import login_required
#from oauth2_provider.decorators import protected_resource
#import json
#from django.contrib.auth.models import User




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from core.users.models import ActiveUser
from core.users.serializers import ActiveUserSerializer


# utilizzato per risolvere il problema dell'accesso concorrente agli item
import threading
edit_lock = threading.Lock();


# methods used to list all user data or insert a new one
class ActiveUserList(APIView):
    """
    List all existing users or create a new user.
    """
    def get(self, request, format=None):
	"""
	Method used to list all available platform users.
	
	@param request: HttpRequest used to retrieve User data.
        @type request: HttpRequest
	@param format: The format used to serialize objects data, JSON by default.
	@type format: string
	@return: HttpResponse containing all serialized data of retrieved User objects.
        @rtype: HttpResponse
	"""
        users = ActiveUser.objects.all()
        serializer = ActiveUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
	"""
	Method used to create and store a new User object.

	@param request: HttpRequest containing the serialized data that will be used to create a new User object.
        @type request: HttpRequest
	@param format: The format used to serialize objects data, JSON by default.
        @type format: string
	@return: HttpResponse containing the id of the new created User object, error otherwise.
        @rtype: HttpResponse	
	"""
        serializer = ActiveUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# methods used to implement CRUD operations over user data
class ActiveUserDetail(APIView):
    # description returned with HTTP OPTION request
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
	"""
	Method used to obtain user data by his id.
	@param request: HttpRequest containing the updated User field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a User object.
	@type pk: int
	@return: User object retrieved by the provided id, error if it isn't available.
	@rtype: User
	"""
        try:
            return ActiveUser.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
	
	"""
	Method used to return serialized data of a user.

	@param request: HttpRequest containing the updated User field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a User object.
        @type pk: int
	@param format: Format used for data serialization.
	@type format: string
	@return: HttpResponse containing all serialized data of a User, error if it isn't available.
        @rtype: HttpResponse
	"""
        user = self.get_object(pk)
        serializer = ActiveUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
	"""
	Method used to update user information providing
	serialized data.

	@param request: HttpRequest containing the updated User field data.
        @type request: HttpRequest
	@param pk: Primary key used to retrieve a User object.
        @type pk: int
	@param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing all update object data.
        @rtype: HttpResponse
	"""
        with edit_lock:
            user = self.get_object(pk)
            serializer = ActiveUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
	"""
        Method used to delete user information providing his ID.

        @param request: HttpRequest used to delete a specific User.
        @type request: HttpRequest
        @param pk: Primary key used to retrieve a User object.
        @type pk: int
        @param format: Format used for data serialization.
        @type format: string
        @return: HttpResponse containing the result of object deletion.
	@rtype: HttpResponse
        """
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






##########################################################
########## decidere quali dei metodi sequenti mantenere




# This file contains all views which provide the main 
# functionalities to users.
# These functionalities are restricted by user role.


# functions available to all users

def login(request):
	"""
	Method used to login a generic user.
	It must be invoked through a GET HTTP request.
	"""
	# extract user credentials
	username = request.GET.get('username', None)
	password = request.GET.get('password', None)
	user = authenticate(username=username, password=password)
	# check for user login
	if(user and user.is_active):
		login(request, user)
		return HttpResponse(json.dumps({'status' : 'OK', 'user_id' : user.id}))

	return HttpResponse(json.dumps({'status' : 'ERROR'}))


#@protected_resource
def logout(request):
	"""
	Method used to logout a generic user.
	This method could be invoked by any HTTP request.
	"""
	try:
		logout(request)
		return HttpResponse(json.dumps({'status' : 'OK'}))
	except:
		return HttpResponse(json.dumps({'status' : 'ERROR'}))

#@protected_resource
def change_password(request):
	"""
	Method used by a user to change his password.
	This method SHOULD be invoked through a PUT HTTP method.
	"""
	# retrieve the user and change his password
	new_password = request.GET.get('password', None)
	if(new_password and len(new_password) > 0):
		request.user.set_password(new_password)
		request.user.save()
		return HttpResponse(json.dumps({'status' : 'OK'}))

	return HttpResponse(json.dumps({'status' : 'ERROR'}))


