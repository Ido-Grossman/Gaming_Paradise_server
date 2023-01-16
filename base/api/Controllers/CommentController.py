from ..serializers import CommentSerializer
from .imports import *


@api_view(['GET', 'POST'])
def comments(request, post_id):
    if request.method == 'GET':
        # Retrieve all comments for the specified post from the database
        all_comments = Queries.select_spec_join(settings.COMMENT_TABLE, settings.USER_TABLE, 'User_id'
                                                , 'id', ['Post_id'], [post_id],
                                           spec_col=['comment.id', 'comment.content', 'comment.TimestampCreated',
                                                     'comment.Post_id', 'user.UserName'])

        # Serialize the comments to return them in a format that can be easily consumed by the client
        serializer = CommentSerializer(all_comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Retrieve the user's name and comment content from the request data
        try:
            user_name = request.data['User_id']
            content = request.data['Content']
        except:
            return Response("Format isn't correct", status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists in the database
        user = Queries.select_spec(settings.USER_TABLE, ['id'], [user_name])
        if not user:
            return Response("User doesn't exist.", status=status.HTTP_404_NOT_FOUND)

        # Insert the new comment into the database
        columns, values = ["Content", "User_Id", "Post_id", "TimestampCreated"], [content, user_name, post_id]
        Queries.insert(settings.COMMENT_TABLE, columns, values)

        # Return a 201 status code to indicate that the comment was successfully created
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def comment_amounts(request, post_id):
    # Retrieve the number of comments for the specified post
    comment_count = Queries.count(settings.COMMENT_TABLE, ['Post_id'], [post_id])

    # Return the comment count along with some context about the post
    return Response({'post_id': post_id, 'comment_count': comment_count})

