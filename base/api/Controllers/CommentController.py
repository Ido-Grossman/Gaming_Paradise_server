from ..serializers import CommentSerializer
from .imports import *



@api_view(['GET', 'POST'])
def comments(request, post_id):
    # Check if the post exists
    if not Queries.select_spec(settings.POST_TABLE, ['id'], [post_id]):
        return Response("Post doesn't exist.", status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        # Get all the comments for the post
        all_comments = Queries.select_spec_join(settings.COMMENT_TABLE, settings.USER_TABLE, 'User_id'
                                                , 'id', ['Post_id'], [post_id],
                                           spec_col=['comment.id', 'comment.content', 'comment.TimestampCreated',
                                                     'comment.Post_id', 'user.UserName'])
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



@api_view(['GET'])
def comment_amounts(request, post_id):
    # Return the comment count along with some context about the post
    return Response(Queries.count(settings.COMMENT_TABLE, ['Post_id'], [post_id]))

