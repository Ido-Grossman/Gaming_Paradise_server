from ..serializers import GenreSerializer, GenreGameSerializer
from .imports import *


@api_view(['GET'])
def get_genres(request):
    # Get all the distinct genres out of the genres table and returns them.
    controller = QueryController.get_instance()
    rows = controller.get_genres()
    genres = GenreSerializer(rows, many=True)
    return Response(genres.data)


@api_view(['GET'])
def get_genre_games(request, genre):
    # Getting all the games of a specific genre and returns them
    rows = Queries.select_spec(settings.GENRE_TABLE, ['Genre'], [genre], ['GameName_id'])
    serializer = GenreGameSerializer(rows, many=True)
    return Response(serializer.data)
