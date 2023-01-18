from ..serializers import GameSerializer
from .imports import *


@api_view(['GET'])
def get_genres(request):
    genre = [request.GET.get('genre', None)]
    # check if a specific genre is requested
    if genre[0]:
        offset = int(request.GET.get('offset', 0))
        # get all games for the requested genre using a custom function, Queries.select_spec_join,
        # which performs a JOIN on the genre and game table and filters by the genre name
        rows = Queries.select_spec_join(settings.GENRE_TABLE, settings.GAME_TABLE, 'Game_id', 'id', ['Genre'],
                                        [genre], spec_col=['game.*'], offset=offset)
        serializer = GameSerializer(rows, many=True)
        return Response(serializer.data)
    # Else, we return a list of all the genres.
    rows = Queries.select_all(settings.GENRE_TABLE, special='DISTINCT', spec_col=['Genre'])
    genres = {"Genre": [row[0] for row in rows]}
    return Response(genres)
