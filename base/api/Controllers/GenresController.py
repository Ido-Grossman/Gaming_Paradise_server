from ..serializers import GenreSerializer, GenreGameSerializer
from .imports import *


@api_view(['GET'])
def get_genres(request):
    # Get all the distinct genres out of the genres table and returns them.
    controller = QueryController.get_instance()
    genres = controller.get_genres()
    return Response(genres)


@api_view(['GET'])
def get_genre_games(request, genre):
    # Getting all the games of a specific genre and returns them
    rows = Queries.select_spec(settings.GENRE_TABLE, ['Genre'], [genre], ['GameName_id'])
    serializer = GenreGameSerializer(rows, many=True, safe=False)
    return Response(serializer.data)
