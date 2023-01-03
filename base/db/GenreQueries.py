from django.db import connection


def select_all():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT Genre FROM base_genre")
        return cursor.fetchall()


def select_game_genres(game_name):
    column_name = 'Genre'
    with connection.cursor() as cursor:
        query = "SELECT {} FROM base_genre WHERE".format(column_name)
        query += " {} = %s".format('GameName_id')
        cursor.execute(query, [game_name])
        x = cursor.fetchall()
        return x


def select_genre_games(genre_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT GameName_id FROM base_genre WHERE Genre = %s", (genre_name,))
        return cursor.fetchall()
