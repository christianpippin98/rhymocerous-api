"""View module for handling requests about users"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for users
    Arguments:
        serializers
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        #the fields are the columns you want to include in the database
        fields = ('id', 'username', 'email')
        # depth = 2

class Users(ViewSet):

    #handles Get request to list ALL product_types
    def list(self, request):
        user = User.objects.all()

        serializer = UserSerializer(
            user, many = True, context={'request':request})

        return Response(serializer.data)
    
    #handles GET for a single product type
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user,
            context = {'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)