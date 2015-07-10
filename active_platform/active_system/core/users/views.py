"""
This module contain all classes necessary for the definition of a REST API
that could be used to manipulate User, Group, Permission and ContentType objects
through CRUD operations.
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status

from core.users.serializers import UserSerializer, GroupSerializer, PermissionSerializer, ContentTypeSerializer
import json
import logging

# variable used for logging purposes
logger = logging.getLogger('active_log')

    
class UserList(ListCreateAPIView):
    queryset = User.objects.all()  # required for DjangoModelPermissions
    serializer_class = UserSerializer
    paginate_by = 10

    def post(self, request, format=None):
        """
        Method used to create a new User object.
        """
        body = json.loads(request.body)
        body["password"] = make_password(body["password"])
        serializer = UserSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Created a new User object')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Error on creation of a new User object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    queryset = User.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        logger.debug('Requested details for User object with id ' + str(pk))
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Updated data of User object with id ' + str(pk))
            return Response(serializer.data)

        logger.error('Error on data update for User object with id ' + str(pk))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.debug('Requested delete on User object with id ' + str(pk))
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupList(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    paginate_by = 10

    def post(self, request, format=None):
        """
        Method used to create a new Group object.
        """
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Created a new Group object')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Error on creation of new Group object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetail(APIView):
    queryset = Group.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        logger.debug('Requested details for Group object with id ' + str(pk))
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        group = self.get_object(pk)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Updated data of Group object with id ' + str(pk))
            return Response(serializer.data)

        logger.error('Error on data update for Group object with id ' + str(pk))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.debug('Requested delete on Group object with id ' + str(pk))
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionList(ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    paginate_by = 10

    def post(self, request, format=None):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Created a new Permission object')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error('Error on creation of a new Permission object')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class PermissionDetail(APIView):
    queryset = Permission.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        logger.debug('Requested details for Permission object with id ' + str(pk))
        permission = self.get_object(pk)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        permission = self.get_object(pk)
        serializer = PermissionSerializer(permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Updated data for Permission object with id ' + str(pk))
            return Response(serializer.data)

        logger.error('Error on data update for Permission object with id ' + str(pk))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.debug('Requested delete on Permission object with id ' + str(pk))
        permission = self.get_object(pk)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentTypeList(ListCreateAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    paginate_by = 10

        
class ContentTypeDetail(APIView):
    queryset = ContentType.objects.none()  # required for DjangoModelPermissions

    def get_object(self, pk):
        try:
            return ContentType.object.get(pk=pk)
        except ContentType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        logger.debug('Requested delete of ContentType object with id ' + str(pk))
        content_type = self.get_object(pk)
        serializer = ContentTypeSerializer(content_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        content_type = self.get_object(pk)
        serializer = ContentTypeSerializer(content_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Updated data of ContentType object with id ' + str(pk))
            return Response(serializer.data)

        logger.error('Error on data update of ContentType object with id ' + str(pk))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        logger.debug('Requested delete on ContentType object with id ' + str(pk))
        content_type = self.get_object(pk)
        content_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
