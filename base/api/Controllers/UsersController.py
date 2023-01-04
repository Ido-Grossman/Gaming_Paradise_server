from ..serializers import *
from .imports import *


@api_view(['POST'])
def login(request):
    username, password = request.data['UserName'], request.data['Password']

    # Check if the user exists and if the password is correct
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_user WHERE UserName = %s AND Password = %s", [username, password])
    if not Queries.select_spec(settings.USER_TABLE, ['UserName', 'Password'], [username, password]):
        return Response("User doesn't exist or password is wrong", status=status.HTTP_404_NOT_FOUND)

    return Response()


@api_view(['POST'])
def register(request):
    # Creating the user object out of the json data and makes sure it is valid.
    username, password = request.data['UserName'], request.data['Password']

    # with connection.cursor() as cursor:
    #     # Check if the user already exists
    #     cursor.execute("SELECT * FROM base_user WHERE UserName = %s", [username])
    if Queries.select_spec(settings.USER_TABLE, ['UserName'], [username]):
        return Response('User exists', status=status.HTTP_404_NOT_FOUND)

        # If the user doesn't exist, insert a new row into the base_user table
        # cursor.execute("INSERT INTO base_user (UserName, Password) VALUES (%s, %s)", (username, password))
    Queries.insert(settings.USER_TABLE, ['UserName', 'Password'], [username, password])

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def user_games(request, pk):
    # with connection.cursor() as cursor:
        # Check if the user exists
        # cursor.execute("SELECT * FROM base_user WHERE UserName = %s", [pk])
        # user = cursor.fetchone()
    user = Queries.select_spec(settings.USER_TABLE, ['UserName'], [pk])
    if not user:
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # If it's get, return all the games of the user.
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT GameName_id FROM base_usergames WHERE UserName_id = %s", [pk])
        #     game_ids = cursor.fetchall()
        game_ids = Queries.select_spec(settings.USER_GAMES_TABLE, ['UserName_id'], [pk], spec_col=['GameName_id'])
        serializer = GameNameSerializer(game_ids, many=True)
        return Response(serializer.data)
    else:
        game_name = request.data['GameName']
        # Get the game object from the database
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM base_game WHERE Name = %s", [game_name])
        #     game = cursor.fetchone()
            # If the game doesn't exist, return 404 not found
        game = Queries.select_spec(settings.GAME_TABLE, ['Name'], [game_name])
        if not game:
            return Response("Game doesn't exist", status=status.HTTP_404_NOT_FOUND)
        columns, values = ['UserName_id', 'GameName_id'], [user[0], game[0]]
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM base_usergames WHERE UserName_id = %s AND GameName_id = %s",
        #                    [user[0], game[0]])
        if Queries.select_spec(settings.USER_GAMES_TABLE, columns, values):
            # If the user already subscribed to the game, remove it from him
            # cursor.execute("DELETE FROM base_usergames WHERE UserName_id = %s AND GameName_id = %s",
            #                 [user[0], game[0]])
            Queries.delete(settings.USER_GAMES_TABLE, columns, values)
        else:
            # Subscribe the user to this game
            # cursor.execute("INSERT INTO base_usergames (UserName_id, GameName_id) VALUES (%s, %s)",
            #                [user[0], game[0]])
            Queries.insert(settings.USER_GAMES_TABLE, columns, values)

        return Response()
