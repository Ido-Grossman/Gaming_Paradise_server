from django.db import connection


def select_all():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM base_game")
        return cursor.fetchall()


def select_spec(game_name):
    with connection.cursor() as cursor:
        query = "SELECT * FROM base_game WHERE Name = %s"
        cursor.execute(query, (game_name,))
        return cursor.fetchone()
