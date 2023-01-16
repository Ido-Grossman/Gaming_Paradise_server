from .db import *
from django.conf import settings


# This class is a singleton, we have only one instance of this in the server.
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
        # If we didn't get the games already, we select all games from the db and store it in self.games.
        if self.games is None:
            self.games = Queries.select_all(settings.GAME_TABLE)
        # If we already fetched the games, we return them.
        return self.games

    def get_genres(self):
        # If we didn't get the genres already, we select all distinct genres from the db and store it in self.genres.
        if not self.genres:
            rows = Queries.select_all(settings.GENRE_TABLE, special='DISTINCT', spec_col=['Genre'])
            self.genres = {"Genre": [row[0] for row in rows]}
        # If we already fetched the genres, we return them.
        return self.genres

    def get_platforms(self):
        # If we didn't get the platforms already, we select all distinct platforms from the db and store
        # it in self.platforms.
        if not self.platforms:
            rows = Queries.select_all(settings.PLATFORM_TABLE, special='DISTINCT', spec_col=['Platform'])
            self.platforms = {"Platform": [row[0] for row in rows]}
        # If we already fetched the platforms, we return them.
        return self.platforms

    def __init__(self):
        # Makes sure we get only one instance of QueryController.
        if QueryController.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            QueryController.__instance = self
