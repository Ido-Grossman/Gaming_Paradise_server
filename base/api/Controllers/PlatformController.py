from ..serializers import PlatformSerializer, PlatformGameSerializer
from .imports import *

@api_view(['GET'])
def get_platform(request):
    # Get all the distinct platforms from the platform table and return them
    controller = QueryController.get_instance()
    platforms = controller.get_platforms()
    # serializer = PlatformSerializer(platforms, many=True)
    return Response(platforms)

@api_view(['GET'])
def get_platform_games(request, platform):
    # Get all the games that are playable on the given platform
    game_ids = Queries.select_spec('base_platform', ['Platform'], [platform], ['GameName_id'])
    serializer = PlatformGameSerializer(game_ids, many=True)
    return Response(serializer.data)
