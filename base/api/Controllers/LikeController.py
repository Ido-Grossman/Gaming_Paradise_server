from .imports import *

def post_like(post_id, user_name):
    # Check if the user exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_user WHERE UserName = %s", [user_name])
    if not Queries.select_spec(settings.USER_TABLE, ['UserName'], [user_name]):
        # If the user doesn't exist, return 404 not found
        return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # Check if the post exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_post WHERE Id = %s", [post_id])
    if not Queries.select_spec(settings.POST_TABLE, ['Id'], [post_id]):
        # If the post doesn't exist, return 404 not found
        return Response("Object doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # Check if the like already exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_like WHERE UserName_id = %s AND PostId_id = %s", (user_name, post_id))
    if Queries.select_spec(settings.LIKE_TABLE, ['UserName_id', 'PostId_id'], [user_name, post_id]):
        # If the like already exists, delete it
        # cursor.execute("DELETE FROM base_like WHERE UserName_id = %s AND PostId_id = %s", (user_name, post_id))
        Queries.delete(settings.LIKE_TABLE, ['UserName_id', 'PostId_id'], [user_name, post_id])
    else:
        # If the like doesn't exist, insert it
        # cursor.execute("INSERT INTO base_like (UserName_id, PostId_id) VALUES (%s, %s)", (user_name, post_id))
        Queries.insert(settings.LIKE_TABLE, ['UserName_id', 'PostId_id'], [user_name, post_id])
    return Response()


@api_view(['POST', 'GET'])
def likes(request, post_id):
    # Going to the right function depending on the method.
    if request.method == 'GET':
        return Response(Queries.count(settings.LIKE_TABLE, ['PostId_id'], [post_id]))
    else:
        return post_like(post_id, request.data['UserName'])


@api_view(['GET'])
def user_likes(request, post_id, user_name):
    if Queries.select_spec(settings.LIKE_TABLE, ['UserName_id', 'PostId_id'], [user_name, post_id]):
        return Response()
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
