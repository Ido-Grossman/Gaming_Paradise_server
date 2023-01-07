from ..serializers import GameSerializer, ReviewSerializer, GameFullSerializer
from .imports import *


@api_view(['GET'])
def get_game(request, game_name):
    """
    Handles GET requests for a single game.
    """
    game_table, game_col = 'base_game', 'Name'
    genres, platforms = [], []
    # Use a raw SQL query to retrieve the requested game
    game_genres = Queries.select_spec_join(settings.GAME_TABLE, settings.GENRE_TABLE, game_col, 'GameName_id'
                                           , [game_col], [game_name])
    # If no game was found, raise a 404 error
    if not game_genres:
        return Response(status=status.HTTP_404_NOT_FOUND)
    for game_genre in game_genres:
        genres.append(game_genre[8])
    game_platforms = Queries.select_spec_join(settings.GAME_TABLE, settings.PLATFORM_TABLE, game_col, 'GameName_id'
                                              , [game_col], [game_name])
    for game_platform in game_platforms:
        platforms.append(game_platform[8])
    game_details = game_platforms[0]
    game = (game_details[0], game_details[1], game_details[2], game_details[3], game_details[4], game_details[5]
            , game_details[6], genres, platforms)
    # Otherwise, serialize the game and return it in the response
    serializer = GameFullSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def get_games(request):
    """
    Handles GET requests for a list of all games.
    """
    offset = int(request.GET.get('offset', 0))
    offset *= 10
    controller = QueryController.get_instance()
    rows = controller.get_games()[offset:offset + 10]
    # Serialize the games and return them in the response
    serializer = GameSerializer(rows, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_game_reviews(request, game_name):
    """
    Handles GET requests for a list of reviews for a specific game.
    """
    # Use a raw SQL query to retrieve the requested game
    game = Queries.select_spec(settings.GAME_TABLE, ['Name'], [game_name])[0]

    # If no game was found, raise a 404 error
    if not game:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve all reviews for the game
    game_revs = Queries.select_spec(settings.REVIEW_TABLE, ['GameName_id'], [game_name])

    # Serialize the reviews and return them in the response
    serializer = ReviewSerializer(game_revs, many=True)
    return Response(serializer.data)
