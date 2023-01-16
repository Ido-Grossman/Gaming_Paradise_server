from ..serializers import *
from .imports import *


@api_view(['POST'])
def login(request):
    username, password = request.data['UserName'], request.data['Password']
    # Check if the user exists and if the password is correct
    user = Queries.select_spec(settings.USER_TABLE, ['UserName', 'Password'], [username, password])
    # If one of the parameters is wrong, return 404 not found
    if not user:
        return Response("User doesn't exist or password is wrong", status=status.HTTP_404_NOT_FOUND)
    # Else, return the id of the user.
    user_id = str(user[0][0])
    return Response(user_id)


@api_view(['POST'])
def register(request):
    # Creating the user object out of the json data and makes sure it is valid.
    username, password = request.data['UserName'], request.data['Password']
    # If the user already exists, return 404 NOT FOUND
    if Queries.select_spec(settings.USER_TABLE, ['UserName'], [username]):
        return Response('User exists', status=status.HTTP_404_NOT_FOUND)
    # If the user doesn't exist, insert a new row into the base_user table
    Queries.insert(settings.USER_TABLE, ['UserName', 'Password'], [username, password])
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def user_games(request, pk):
    user = Queries.select_spec(settings.USER_TABLE, ['id'], [pk])
    if not user:
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # If it's get, return all the games of the user.
        # game_ids = Queries.select_spec(settings.USER_GAMES_TABLE, ['User_id'], [pk], spec_col=['Game_id'])
        game_ids = Queries.select_spec_join(settings.USER_GAMES_TABLE, settings.GAME_TABLE, 'Game_id', 'id',
                                            ['User_id'], [pk], spec_col=['game.*'])
        serializer = GameSerializer(game_ids, many=True)
        return Response(serializer.data)
    else:
        game_id = request.data['Game_id']
        # Get the game object from the database
        game = Queries.select_spec(settings.GAME_TABLE, ['id'], [game_id])
        if not game:
            return Response("Game doesn't exist", status=status.HTTP_404_NOT_FOUND)
        columns, values = ['User_id', 'Game_id'], [user[0][0], game[0][0]]
        if Queries.select_spec(settings.USER_GAMES_TABLE, columns, values):
            # If the user already subscribed to the game, remove it from him
            Queries.delete(settings.USER_GAMES_TABLE, columns, values)
        else:
            # Subscribe the user to this game
            Queries.insert(settings.USER_GAMES_TABLE, columns, values)
        return Response()


@api_view(['GET'])
def user_game(request, user_id, game_id):
    # Gets a specific game from the usergames of the user id.
    row = Queries.select_spec(settings.USER_GAMES_TABLE, ['User_id', 'Game_id'], [user_id, game_id])
    # If the user didn't subscribe to the game, return 404 NOT FOUND.
    if not row:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # If the user subscribed to the game, return 200.
    return Response(status=status.HTTP_200_OK)
