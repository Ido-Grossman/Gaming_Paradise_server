from ..serializers import ReviewSerializer
from .imports import *

@api_view(['POST'])
def create_review(request):
    # Getting the data of the request.
    review = request.data
    user_name, game_name, rev = review['UserName'], review['GameName'], review['Review']

    # Check if the game exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_game WHERE Name=%s", [game_name])

    x = settings.GAME_TABLE
    if not Queries.select_spec(settings.GAME_TABLE, ['Name'], [game_name]):
        # If the game doesn't exist it returns 404 not found
        return Response("Game doesn't exist.", status=status.HTTP_404_NOT_FOUND)

    # Create the review
    # with connection.cursor() as cursor:
    #     cursor.execute("INSERT INTO base_review (UserName, GameName_id, Review, TimestampCreated) VALUES (%s, %s, %s, NOW())", [user_name, game_name, rev])
    columns, values = ['UserName', 'GameName_id', 'Review', 'TimestampCreated'], [user_name, game_name, rev]
    Queries.insert(settings.REVIEW_TABLE, columns, values)

    return Response()

@api_view(['GET', 'PUT', 'DELETE'])
def specific_review(request, rev_id):
    # Check if the review exists
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM base_review WHERE RecommendationId = %s", [rev_id])
    #     review = cursor.fetchone()
    review = Queries.select_spec(settings.REVIEW_TABLE, ['RecommendationId'], [rev_id])
    if not review:
        # If the review doesn't exist, return 404 not found
        return Response("Review doesn't exist", status=status.HTTP_404_NOT_FOUND)
    review = review[0]
    if request.method == 'GET':
        # Use the ReviewSerializer to convert the review data into JSON
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Make sure the user who is requesting to change the data is the user who wrote the review
        if review[1] != request.data['UserName']:
            return Response("You aren't allowed to edit this review.", status=status.HTTP_400_BAD_REQUEST)
        # Update the review
        # with connection.cursor() as cursor:
        #     cursor.execute("UPDATE base_review SET Review = %s WHERE RecommendationId = %s", [request.data['Review'], rev_id])
        Queries.update(settings.REVIEW_TABLE, ['Review'], [request.data['Review']], ['RecommendationId'], [rev_id])
    else:
        # Delete the review
        # with connection.cursor() as cursor:
        #     cursor.execute("DELETE FROM base_review WHERE RecommendationId = %s", [rev_id])
        Queries.delete(settings.REVIEW_TABLE, ['RecommendationId'], [rev_id])
    return Response()
