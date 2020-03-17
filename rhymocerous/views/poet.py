"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rhymocerous.models import Poet


class PoetSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for poets

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Poet
        url = serializers.HyperlinkedIdentityField(
            view_name='poet',
            lookup_field='id'
        )
        fields = ('id', 'user')


class Poets(ViewSet):
    """Poets for Rhymocerous"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single poet

        Returns:
            Response -- JSON serialized poet instance
        """
        try:
            poet = Poet.objects.get(pk=pk)
            serializer = PoetSerializer(poet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to poets resource

        Returns:
            Response -- JSON serialized list of poets
        """
        poets = Poet.objects.all()
        serializer = PoetSerializer(
            poets,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)