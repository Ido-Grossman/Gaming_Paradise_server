from ..serializers import PostSerializer
from .imports import *

post_table = 'base_post '


@api_view(['GET'])
def get_user_posts(request, pk):
    # Get all the posts of the specific user and return them.
    user_posts_query = Queries.select_spec('base_post', 'UserName_id', pk)
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_post WHERE UserName_id = %s", [pk])
    #     user_posts = cursor.fetchall()
    serializer = PostSerializer(user_posts_query, many=True)
    return Response(serializer.data)


@api_view(['PUT', 'GET', 'DELETE'])
def user_post(request, pk):
    # Check if the post exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_post WHERE Id = %s", [pk])
    #     post = cursor.fetchone()
    post = Queries.select_spec(settings.POST_TABLE, ["Id"], [pk])[0]
    if not post:
        return Response("Post doesn't exist", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # Return the post
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Make sure the user who is requesting to change the data is the user who wrote the post
        if post[5] != request.data['UserName']:
            return Response("This user didn't write this post", status=status.HTTP_404_NOT_FOUND)
        # Update the title and content of the post
        # with connection.cursor() as cursor:
        #     cursor.execute("UPDATE base_post SET Title = %s, Content = %s WHERE Id = %s", [request.data['Title'], request.data['Content'], pk])
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
    # serializer = PostSerializer(data=request.data)
    # # Making sure the json was valid
    # if not serializer.is_valid():
    #     return Response("The details weren't correct", status=status.HTTP_404_NOT_FOUND)
    post_data = request.data
    user_name = post_data['UserName']
    game_name = post_data['GameName']
    content = post_data['Content']
    title = post_data['Title']

    # Check if the user and game exist
    # cursor.execute("SELECT * FROM base_user WHERE UserName = %s", [user_name])
    if not Queries.select_spec(settings.USER_TABLE, ['UserName'], [user_name]):
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)
    # cursor.execute("SELECT * FROM base_game WHERE Name = %s", [game_name])
    if not Queries.select_spec(settings.GAME_TABLE, ['Name'], [game_name]):
        # If the game doesn't exist, return 404 not found
        return Response("Game doesn't exist.", status=status.HTTP_404_NOT_FOUND)

# Insert the post into the database
#     cursor.execute("INSERT INTO base_post (Content, Title, UserName_id, GameName_id, TimestampCreated) VALUES (%s, %s, %s, %s, NOW())", [content, title, user_name, game_name])
    columns = ['Content', 'Title', 'UserName_id', 'GameName_id', 'TimestampCreated']
    values = [content, title, user_name, game_name]
    Queries.insert(settings.POST_TABLE, columns, values)
    return Response(status=status.HTTP_201_CREATED)

"""
{
"UserName": "Idog770",
"GameName": "Subnautica",
"Content": "Strange bug this is",
"Title": "What a strange bug"
}
"""


@api_view(['GET'])
def popular_posts(request):
    offset = int(request.GET.get('offset', 0))
    posts = Queries.select_recent(offset=offset)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_game_posts(request, game_name):
    offset = int(request.GET.get('offset', 0))
    posts = Queries.select_recent_game(game_name, offset=offset)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_user_posts(request, user_name):
    offset = int(request.GET.get('offset', 0))
    posts = Queries.select_recent_user(user_name, offset=offset)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
