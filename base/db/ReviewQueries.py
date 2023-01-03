from django.db import connection


def get_game_reviews(game_name):
    with connection.cursor() as cursor:
        query = "SELECT * FROM base_review WHERE GameName_id = %s"
        cursor.execute(query,(game_name,))
        return cursor.fetchall()
