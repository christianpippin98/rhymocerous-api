"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rhymocerous.models import Poem


class PoemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for poems

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Poem
        url = serializers.HyperlinkedIdentityField(
            view_name='poem',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'body', 'poet', 'createdAt')


class Poems(ViewSet):
    """Poems for Rhymocerous"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single poem

        Returns:
            Response -- JSON serialized poem instance
        """
        try:
            poem = Poem.objects.get(pk=pk)
            serializer = PoemSerializer(poem, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    def list(self, request):
        """Handle GET requests to poems resource

        Returns:
            Response -- JSON serialized list of poems
        """
        poems = Poem.objects.all()
        serializer = PoemSerializer(
            poems,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)