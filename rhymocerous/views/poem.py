from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rhymocerous.models import Poem, Poet


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
        depth = 2


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

    def create(self, request):
        new_poem = Poem()
        new_poem.title = request.data["title"]
        new_poem.poet = Poet.objects.get(user=request.auth.user.id)
        new_poem.body = request.data["body"]

        new_poem.save()

        serializer = PoemSerializer(new_poem, context={'request': request})

        return Response(serializer.data)

    # handles PUT
    def update(self, request, pk=None):
      """Handle PUT requests for a poem
      Returns:
          Response -- Empty body with 204 status code
      """
      poem = Poem.objects.get(pk=pk)
      poem.title = request.data["title"]
      poem.body = request.data["body"]
      poem.save()

      return Response({}, status=status.HTTP_204_NO_CONTENT)

    # handles DELETE
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single poem
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            poem = Poem.objects.get(pk=pk)
            poem.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Poem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)