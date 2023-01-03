from django.db import connection


def select_all():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT Platform FROM base_platform")
        return cursor.fetchall()


def select_game_platforms(game_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Platform FROM (SELECT * FROM base_platform WHERE GameName_id = %s) as `bg*`", (game_name,))
        return cursor.fetchall()


def select_platform_games(platform_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT GameName_id FROM base_platform WHERE Platform = %s", (platform_name,))
        return cursor.fetchall()
