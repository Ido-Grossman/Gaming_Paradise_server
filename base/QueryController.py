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
            rows = Queries.select_all(settings.GENRE_TABLE, special='DISTINCT', spec_col=['Genre'])
            self.genres = {"Genre" : [row[0] for row in rows]}
        return self.genres


    def get_platforms(self):
        if not self.platforms:
            rows = Queries.select_all(settings.PLATFORM_TABLE, special='DISTINCT', spec_col=['Platform'])
            self.platforms = {"Platform" : [row[0] for row in rows]}
        return self.platforms

    def __init__(self):
        if QueryController.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            QueryController.__instance = self
