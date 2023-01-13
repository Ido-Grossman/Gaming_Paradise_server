from ..serializers import GameSerializer, ReviewSerializer, GameFullSerializer
from .imports import *


@api_view(['GET'])
def get_game(request, game_id):
    """
    Handles GET requests for a single game.
    """
    game_col = 'id'
    genres, platforms = [], []
    # Use a raw SQL query to retrieve the requested game
    game_genres = Queries.select_spec_join(settings.GENRE_TABLE, settings.GAME_TABLE, 'Game_id',
                                           'id', [settings.GAME_TABLE + "." + game_col], [game_id])
    # If no game was found, raise a 404 error
    for game_genre in game_genres:
        genres.append(game_genre[8])
    game_platforms = Queries.select_spec_join(settings.GAME_TABLE, settings.PLATFORM_TABLE, game_col, 'Game_id'
                                              , [settings.GAME_TABLE + "." + game_col], [game_id])
    for game_platform in game_platforms:
        platforms.append(game_platform[8])
    game_details = game_platforms[0]
    game = (game_details[0], game_details[1], game_details[2], game_details[3], game_details[4], game_details[5]
            , game_details[6], game_details[7], genres, platforms)
    # Otherwise, serialize the game and return it in the response
    serializer = GameFullSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def get_games(request):
    """
    Handles GET requests for a list of all games.
    """
    offset = int(request.GET.get('offset', 0))
    game = [request.GET.get('game', None)]
    if game[0]:
        game[0] = '%' + game[0] + '%'
        where = ['Name']
        games = Queries.select_spec(settings.GAME_TABLE, where, [game], like_cols=where, offset=offset)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    offset *= 100
    controller = QueryController.get_instance()
    rows = controller.get_games()[offset:offset + 100]
    # Serialize the games and return them in the response
    serializer = GameSerializer(rows, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_game_reviews(request, game_id):
    """
    Handles GET requests for a list of reviews for a specific game.
    """
    # Use a raw SQL query to retrieve the requested game
    game = Queries.select_spec(settings.GAME_TABLE, ['id'], [game_id])

    # If no game was found, raise a 404 error
    if not game:
        return Response(status=status.HTTP_404_NOT_FOUND)
    game = game[0]
    offset = int(request.GET.get('offset', 0))

    # Retrieve all reviews for the game
    game_revs = Queries.select_spec(settings.REVIEW_TABLE, ['Game_id'], [game_id], offset=offset)
    if len(game_revs) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Serialize the reviews and return them in the response
    serializer = ReviewSerializer(game_revs, many=True)
    return Response(serializer.data)
