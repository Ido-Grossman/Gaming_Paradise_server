from ..serializers import PostSerializer
from .imports import *


@api_view(['GET'])
def get_user_posts(request, pk):
    columns = [".id", ".TimestampCreated", ".Content", ".Title"]
    # add the table name to each column for the query
    for i in range(4):
        columns[i] = settings.POST_TABLE + columns[i]
    columns.append("game.Name")
    columns.append("user.UserName")
    # get all posts made by the user using a custom function, Queries.select_spec_join,
    # which performs a JOIN on the post, game, and user table and filters by the user id
    user_posts_query = Queries.select_spec_join(settings.POST_TABLE, settings.GAME_TABLE, 'Game_id', "id", ["User_id"],
                                                pk, table3=settings.USER_TABLE, table3_col='id', table1_col2="User_id",
                                                spec_col=columns)
    serializer = PostSerializer(user_posts_query, many=True)
    return Response(serializer.data)



@api_view(['PUT', 'GET', 'DELETE'])
def user_post(request, pk):
    # Gets the posts from the database.
    post = Queries.select_spec(settings.POST_TABLE, ["id"], [pk])[0]
    # If the posts don't exist, it returns 404.
    if not post:
        return Response("Post doesn't exist", status=status.HTTP_404_NOT_FOUND)
    # If this is a get request, we return the details of the post.
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    # If it's a put request, we update the details of the post, only if the user is the user who wrote it.
    elif request.method == 'PUT':
        if post[5] != int(request.data['User_id']):
            return Response("This user didn't write this post", status=status.HTTP_404_NOT_FOUND)
        columns, values = ['Title', 'Content'], [request.data['Title'], request.data['Content']]
        Queries.update(settings.POST_TABLE, columns, values, ['Id'], [pk])
    # If we get a delete request, we delete the post.
    elif request.method == 'DELETE':
        Queries.delete(settings.POST_TABLE, ['Id'], [pk])
    return Response()

@api_view(['POST'])
def create_post(request):
    # Creating a post object out of the json data that was sent.
    post_data = request.data
    # Getting the post parameters from the post request.
    try:
        user_name = post_data['UserId']
        game_name = post_data['GameId']
        content = post_data['Content']
        title = post_data['Title']
    except KeyError:
        # If one of the parameters is missing we return 400 BAD REQUEST.
        return Response("One of the parameters are missing", status=status.HTTP_400_BAD_REQUEST)
    # Check if the user and game exist
    if not Queries.select_spec(settings.USER_TABLE, ['id'], [user_name]):
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)
    if not Queries.select_spec(settings.GAME_TABLE, ['id'], [game_name]):
        # If the game doesn't exist, return 404 not found
        return Response("Game doesn't exist.", status=status.HTTP_404_NOT_FOUND)
    # Insert the post into the database
    columns = ['Content', 'Title', 'User_id', 'Game_id', 'TimestampCreated']
    values = [content, title, user_name, game_name]
    Queries.insert(settings.POST_TABLE, columns, values)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def popular_posts(request):
    # Gets the offset and day from the request.
    offset = int(request.GET.get('offset', 0))
    # Gets the popular posts in the requested offset.
    posts = Queries.select_recent(offset=offset)
    # If there are no more posts, return 204 NO CONTENT
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    # return the posts.
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_game_posts(request, game_name):
    # Gets the offset and day from the request.
    offset = int(request.GET.get('offset', 0))
    # Gets the popular posts in the requested offset, about the specific game.
    posts = Queries.select_recent_game(game_name, offset=offset)
    # If there are no more posts, return 204 NO CONTENT
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    # return the posts.
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_user_posts(request, user_name):
    # Gets the offset and day from the request.
    offset = int(request.GET.get('offset', 0))
    day = int(request.GET.get('day', 0))
    # Gets the popular posts in the requested offset, about the specific user games.
    posts = Queries.select_recent_user(user_name, offset=offset)
    # If there are no more posts, return 204 NO CONTENT
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    # return the posts.
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
