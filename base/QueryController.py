from .db import *
from django.conf import settings


class QueryController:
    __instance = None
    games = None
    genres = None
    platforms = None

    @staticmethod
    def get_instance():
        if QueryController.__instance is None:
            QueryController()
        return QueryController.__instance

    def get_games(self):
        if self.games is None:
            self.games = Queries.select_all(settings.GAME_TABLE)
        return self.games


    def get_genres(self):
        if not self.genres:
            self.genres = Queries.select_all('base_genre', special='DISTINCT', spec_col=['Genre'])
        return self.genres


    def get_platforms(self):
        if not self.platforms:
            self.platforms = Queries.select_all('base_platform', special='DISTINCT', spec_col=['Platform'])
        return self.platforms

    def __init__(self):
        if QueryController.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            QueryController.__instance = self
