from ..serializers import GameSerializer, ReviewSerializer, GameFullSerializer
from .imports import *


@api_view(['GET'])
def get_game(request, game_id):
    game_col = 'id'
    genres, platforms = [], []
    # If no game was found, raise a 404 error
    if not Queries.select_spec(settings.GAME_TABLE, [game_col], [game_id]):
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Use a raw SQL query to retrieve the requested game
    game_genres = Queries.select_spec_join(settings.GAME_TABLE, settings.GENRE_TABLE, game_col, 'Game_id',
                                           [settings.GAME_TABLE + "." + game_col], [game_id])
    for game_genre in game_genres:
        genres.append(game_genre[9])
    game_platforms = Queries.select_spec_join(settings.GAME_TABLE, settings.PLATFORM_TABLE, game_col, 'Game_id'
                                              , [settings.GAME_TABLE + "." + game_col], [game_id])
    for game_platform in game_platforms:
        platforms.append(game_platform[9])
    game_details = game_platforms[0]
    game = (game_details[0], game_details[1], game_details[2], game_details[3], game_details[4], game_details[5]
            , game_details[6], game_details[7], genres, platforms)
    # Otherwise, serialize the game and return it in the response
    serializer = GameFullSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def get_games(request):
    # Gets the offset from the get request, if no offset is sent, it sets it as 0.
    offset = int(request.GET.get('offset', 0))
    # Tries to get a game name from the get request, if none is sent it sets it as none.
    game = [request.GET.get('game', None)]
    # If a game name is sent, we return only the games which contains the name of the game that was sent.
    if game[0]:
        game[0] = '%' + game[0] + '%'
        where = ['Name']
        games = Queries.select_spec(settings.GAME_TABLE, where, [game], like_cols=where, offset=offset)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    # If no game was sent, we retrieve all the game in offsets of 100.
    controller = QueryController.get_instance()
    rows = Queries.select_all(settings.GAME_TABLE, offset=offset)
    # Serialize the games and return them in the response
    serializer = GameSerializer(rows, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_game_reviews(request, game_id):
    # Tries to get the specific game from the DB, if the game doesn't exist it returns NOT FOUND.
    game = Queries.select_spec(settings.GAME_TABLE, ['id'], [game_id])
    if not game:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Gets the offset from the get request, if none was sent it sets it as 0
    offset = int(request.GET.get('offset', 0))
    # Gets all the reviews of the game with the offset.
    game_revs = Queries.select_spec(settings.REVIEW_TABLE, ['Game_id'], [game_id], offset=offset)
    # If there are no more reviews it returns NO CONTENT.
    if len(game_revs) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    # Returns all the reviews in the current offset.
    serializer = ReviewSerializer(game_revs, many=True)
    return Response(serializer.data)
