from ..serializers import GameSerializer
from .imports import *


@api_view(['GET'])
def get_genres(request):
    # Get all the distinct genres out of the genres table and returns them.
    genre = request.GET.get('genre', None)
    if genre:
        offset = int(request.GET.get('offset', 0))
        rows = Queries.select_spec_join(settings.GENRE_TABLE, settings.GAME_TABLE, 'Game_id', 'id', ['Genre'],
                                        [genre], spec_col=['game.*'], offset=offset)
        serializer = GameSerializer(rows, many=True)
        return Response(serializer.data)
    controller = QueryController.get_instance()
    genres = controller.get_genres()
    return Response(genres)


@api_view(['GET'])
def get_genre_games(request, genre):
    # Getting all the games of a specific genre and returns them
    rows = Queries.select_spec(settings.GENRE_TABLE, ['Genre'], [genre], ['Game_id'])
    serializer = GenreGameSerializer(rows, many=True)
    return Response(serializer.data)
