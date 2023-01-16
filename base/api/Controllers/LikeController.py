from .imports import *

def post_like(post_id, user_id):
    # Check if the user exists
    if not Queries.select_spec(settings.USER_TABLE, ['id'], [user_id]):
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # Check if the post exists
    if not Queries.select_spec(settings.POST_TABLE, ['id'], [post_id]):
        # If the post doesn't exist, return 404 not found
        return Response("Object doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # Check if the like already exists
    if Queries.select_spec(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id]):
        # If the like already exists, delete it
        Queries.delete(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id])
    else:
        # If the like doesn't exist, insert it
        Queries.insert(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id])
    return Response()


@api_view(['POST', 'GET'])
def likes(request, post_id):
    # Going to the right function depending on the method.
    if request.method == 'GET':
        return Response(Queries.count(settings.LIKE_TABLE, ['Post_id'], [post_id]))
    else:
        return post_like(post_id, request.data['User_id'])


@api_view(['GET'])
def user_likes(request, post_id, user_id):
    if Queries.select_spec(settings.LIKE_TABLE, ['User_id', 'Post_id'], [user_id, post_id]):
        return Response()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)