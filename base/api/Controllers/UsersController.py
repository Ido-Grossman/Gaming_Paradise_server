from ..serializers import *
from .imports import *


@api_view(['POST'])
def login(request):
    username, password = request.data['UserName'], request.data['Password']

    # Check if the user exists and if the password is correct
    if not Queries.select_spec(settings.USER_TABLE, ['UserName', 'Password'], [username, password]):
        return Response("User doesn't exist or password is wrong", status=status.HTTP_404_NOT_FOUND)
    return Response()


@api_view(['POST'])
def register(request):
    # Creating the user object out of the json data and makes sure it is valid.
    username, password = request.data['UserName'], request.data['Password']

    if Queries.select_spec(settings.USER_TABLE, ['UserName'], [username]):
        return Response('User exists', status=status.HTTP_404_NOT_FOUND)

    # If the user doesn't exist, insert a new row into the base_user table
    Queries.insert(settings.USER_TABLE, ['UserName', 'Password'], [username, password])

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def user_games(request, pk):
    user = Queries.select_spec(settings.USER_TABLE, ['UserName'], [pk])
    if not user:
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # If it's get, return all the games of the user.
        game_ids = Queries.select_spec(settings.USER_GAMES_TABLE, ['UserName_id'], [pk], spec_col=['GameName_id'])
        serializer = GameNameSerializer(game_ids, many=True)
        return Response(serializer.data)
    else:
        game_name = request.data['GameName']
        # Get the game object from the database
        game = Queries.select_spec(settings.GAME_TABLE, ['Name'], [game_name])
        if not game:
            return Response("Game doesn't exist", status=status.HTTP_404_NOT_FOUND)
        columns, values = ['UserName_id', 'GameName_id'], [user[0], game[0]]
        if Queries.select_spec(settings.USER_GAMES_TABLE, columns, values):
            # If the user already subscribed to the game, remove it from him
            Queries.delete(settings.USER_GAMES_TABLE, columns, values)
        else:
            # Subscribe the user to this game
            Queries.insert(settings.USER_GAMES_TABLE, columns, values)

        return Response()


@api_view(['GET'])
def user_game(request, user_name, game_name):
    row = Queries.select_spec(settings.USER_GAMES_TABLE, ['UserName_id', 'GameName_id'], [user_name, game_name])
    if not row:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)
