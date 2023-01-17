from ..serializers import ReviewSerializer
from .imports import *

@api_view(['GET', 'PUT', 'DELETE'])
def specific_review(request, rev_id):
    # Check if the review exists
    review = Queries.select_spec(settings.REVIEW_TABLE, ['id'], [rev_id])
    if not review:
        # If the review doesn't exist, return 404 not found
        return Response("Review doesn't exist", status=status.HTTP_404_NOT_FOUND)
    review = review[0]
    # Use the ReviewSerializer to convert the review data into JSON
    serializer = ReviewSerializer(review)
    return Response(serializer.data)
