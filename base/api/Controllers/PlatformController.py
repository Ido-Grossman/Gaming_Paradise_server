from ..serializers import GameSerializer
from .imports import *

@api_view(['GET'])
def get_platform(request):
    platform = [request.GET.get('platform', None)]
    # check if a specific platform is requested
    if platform[0]:
        offset = int(request.GET.get('offset', 0))
        # get all games for the requested platform using a custom function, Queries.select_spec_join,
        # which performs a JOIN on the platform and game table and filters by the platform name
        game_ids = Queries.select_spec_join(settings.PLATFORM_TABLE, settings.GAME_TABLE, 'Game_id', 'id', ['Platform'],
                                            [platform], spec_col=['game.*'], offset=offset)
        serializer = GameSerializer(game_ids, many=True)
        return Response(serializer.data)
    # If no platform is requested, it returns all the distinct platforms.
    rows = Queries.select_all(settings.PLATFORM_TABLE, special='DISTINCT', spec_col=['Platform'])
    platforms = {"Platform": [row[0] for row in rows]}
    return Response(platforms)
