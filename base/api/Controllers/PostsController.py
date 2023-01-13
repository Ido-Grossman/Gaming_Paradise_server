from ..serializers import PostSerializer
from .imports import *

post_table = 'base_post '


@api_view(['GET'])
def get_user_posts(request, pk):
    # Get all the posts of the specific user and return them.
    user_posts_query = Queries.select_spec(settings.POST_TABLE, ['User_id'], [pk])
    serializer = PostSerializer(user_posts_query, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'GET', 'DELETE'])
def user_post(request, pk):
    # Check if the post exists
    post = Queries.select_spec(settings.POST_TABLE, ["id"], [pk])[0]
    if not post:
        return Response("Post doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # Return the post
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Make sure the user who is requesting to change the data is the user who wrote the post
        if post[5] != int(request.data['User_id']):
            return Response("This user didn't write this post", status=status.HTTP_404_NOT_FOUND)
        # Update the title and content of the post
        columns, values = ['Title', 'Content'], [request.data['Title'], request.data['Content']]
        Queries.update(settings.POST_TABLE, columns, values, ['Id'], [pk])
    else:
        # Delete the post
        # with connection.cursor() as cursor:
        #     cursor.execute("DELETE FROM base_post WHERE Id = %s", [pk])
        Queries.delete(settings.POST_TABLE, ['Id'], [pk])
    return Response()

@api_view(['POST'])
def create_post(request):
    # Creating a post object out of the json data that was sent.
    post_data = request.data
    try:
        user_name = post_data['UserId']
        game_name = post_data['GameId']
        content = post_data['Content']
        title = post_data['Title']
    except KeyError:
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

"""
{
"UserId": "1",
"GameId": "9",
"Content": "Strange bug this is",
"Title": "What a strange bug"
}
"""


@api_view(['GET'])
def popular_posts(request):
    offset = int(request.GET.get('offset', 0))
    day = int(request.GET.get('day', 0))
    posts = Queries.select_recent(day, offset=offset)
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_game_posts(request, game_name):
    offset = int(request.GET.get('offset', 0))
    day = int(request.GET.get('day', 0))
    posts = Queries.select_recent_game(day, game_name, offset=offset)
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_user_posts(request, user_name):
    offset = int(request.GET.get('offset', 0))
    day = int(request.GET.get('day', 0))
    posts = Queries.select_recent_user(user_name, day, offset=offset)
    if len(posts) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
