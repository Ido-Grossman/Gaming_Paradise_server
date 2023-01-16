from ..serializers import GameSerializer, ReviewSerializer, GameFullSerializer
from .imports import *


@api_view(['GET'])
def get_game(request, game_id):
    game_col = 'id' # column name for the game id
    genres, platforms = [], [] # empty lists to store the game's genres and platforms
    # get all genres for the game using a custom function, Queries.select_spec_join,
    # which performs a JOIN on the genre and game table and filters by the game id
    game_genres = Queries.select_spec_join(settings.GENRE_TABLE, settings.GAME_TABLE, 'Game_id',
                                           'id', [settings.GAME_TABLE + "." + game_col], [game_id])
    for game_genre in game_genres:
        # add each genre to the genres list
        genres.append(game_genre[8])
    # get all platforms for the game using a custom function, Queries.select_spec_join,
    # which performs a JOIN on the platform and game table and filters by the game id
    game_platforms = Queries.select_spec_join(settings.GAME_TABLE, settings.PLATFORM_TABLE, game_col, 'Game_id'
                                              , [settings.GAME_TABLE + "." + game_col], [game_id])
    for game_platform in game_platforms:
        # add each platform to the platforms list
        platforms.append(game_platform[8])
    game_details = game_platforms[0]
    # create a tuple for the game containing all the details and the genres and platforms lists
    game = (game_details[0], game_details[1], game_details[2], game_details[3], game_details[4], game_details[5]
            , game_details[6], game_details[7], genres, platforms)
    serializer = GameFullSerializer(game)
    # use the serializer to convert the game data to json format
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
    offset *= 100
    controller = QueryController.get_instance()
    rows = controller.get_games()[offset:offset + 100]
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
