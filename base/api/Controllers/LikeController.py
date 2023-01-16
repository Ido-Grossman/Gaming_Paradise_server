from .imports import *

def post_like(post_id, user_id):
    # check if user exists
    if not Queries.select_spec(settings.USER_TABLE, ['id'], [user_id]):
        return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # check if post exists
    if not Queries.select_spec(settings.POST_TABLE, ['id'], [post_id]):
        return Response("Object doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # check if the user has already liked the post
    if Queries.select_spec(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id]):
        # if they have, delete the like
        Queries.delete(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id])
    else:
        # if they haven't, insert a new like
        Queries.insert(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id])
    return Response()


@api_view(['POST', 'GET'])
def likes(request, post_id):
    if request.method == 'GET':
        # Handles GET request for counting the number of likes on a post.
        x = Queries.count(settings.LIKE_TABLE, ['Post_id'], [post_id])
        return Response(x)
    else:
        # Handles POST request for like actions on a post
        return post_like(post_id, request.data['User_id'])


@api_view(['GET'])
def user_likes(request, post_id, user_id):
    # check if the user has liked the post
    if Queries.select_spec(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id]):
        return Response()
    else:
        # if they haven't, return a 404 not found response
        return Response(status=status.HTTP_404_NOT_FOUND)
