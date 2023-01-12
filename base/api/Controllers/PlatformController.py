from ..serializers import GameSerializer
from .imports import *

@api_view(['GET'])
def get_platform(request):
    # Get all the distinct platforms from the platform table and return them
    platform = [request.GET.get('platform', None)]
    if platform[0]:
        offset = int(request.GET.get('offset', 0))
        game_ids = Queries.select_spec_join(settings.PLATFORM_TABLE, settings.GAME_TABLE, 'Game_id', 'id', ['Platform'],
                                            [platform], spec_col=['game.*'], offset=offset)
        serializer = GameSerializer(game_ids, many=True)
        return Response(serializer.data)
    controller = QueryController.get_instance()
    platforms = controller.get_platforms()
    return Response(platforms)
