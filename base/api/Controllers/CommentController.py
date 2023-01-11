from ..serializers import CommentSerializer
from .imports import *


@api_view(['GET', 'POST'])
def comments(request, post_id):
    # Check if the post exists
    if not Queries.select_spec(settings.POST_TABLE, ['id'], [post_id]):
        return Response("Post doesn't exist.", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # Get all the comments for the post
        all_comments = Queries.select_spec(settings.COMMENT_TABLE, ['Post_id'], [post_id])
        serializer = CommentSerializer(all_comments, many=True)
        return Response(serializer.data)
    else:
        # If the method is POST, create a new comment
        user_name = request.data['User_id']
        content = request.data['Content']
        # Check if the user exists
        user = Queries.select_spec(settings.USER_TABLE, ['id'], [user_name])
        if not user:
            return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)
        # Insert the comment into the database
        columns, values = ["Content", "User_Id", "Post_id", "TimestampCreated"], [content, user_name, post_id]
        Queries.insert(settings.COMMENT_TABLE, columns, values)
        return Response()


# @api_view(['GET', 'PUT', 'DELETE'])
# def spec_comment(request, post_id, comment_id):
#     # Check if the post and comment exist
#     if not Queries.select_spec(settings.POST_TABLE, ['Id'], [post_id]):
#         # If the post doesn't exist, return 404 not found
#         return Response("Post doesn't exist.", status=status.HTTP_404_NOT_FOUND)
#     comment = Queries.select_spec(settings.COMMENT_TABLE, ['CommentId', 'PostId_id'], [comment_id, post_id])
#     if not comment:
#         # If the comment doesn't exist, return 404 not found
#         return Response("Comment doesn't exist.", status=status.HTTP_404_NOT_FOUND)
#     comment = comment[0]
#     if request.method == 'GET':
#         # If the method is GET, retrieve the comment from the database
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#     columns, values = ['CommentId', 'PostId_id'], [comment_id, post_id]
#     if request.method == "PUT":
#         comment_user = comment[3]
#         if comment_user != request.data['UserName']:
#             return Response("You aren't allowed to edit this comment.", status=status.HTTP_400_BAD_REQUEST)
#         # If the method is PUT, update the comment in the database
#         Queries.update(settings.COMMENT_TABLE, ['Content'], [request.data['Content']], columns, values)
#     else:
#         # If the method is DELETE, delete the comment from the database
#         Queries.delete(settings.COMMENT_TABLE, columns, values)
#     return Response()


@api_view(['GET'])
def comment_amounts(request, post_id):
    return Response(Queries.count(settings.COMMENT_TABLE, ['Post_id'], [post_id]))
