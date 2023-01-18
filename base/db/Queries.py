from django.db import connection


def build_query(table_name, columns, special=None):
    # Start building the SELECT query
    query = "SELECT "
    # If special is provided, add it to the query
    if special:
        query += special
    # If no columns are provided, select all columns from the table
    if not columns:
        query += " * FROM {}".format(table_name)
    # If columns are provided, select them from the table
    else:
        # Calculate the size of the columns list
        size = len(columns)
        # Iterate through the columns, except for the last one
        for i in range(size - 1):
            query += " {},".format(columns[i])
        # Add the last column
        query += " {}".format(columns[size - 1])
        # Add the table name to the query
        query += " FROM {}".format(table_name)
    # Return the constructed query
    return query


def add_offset(offset):
    # Multiply the offset by 100, and get the rows from offset * 100 to (offset * 100) + 100
    offset *= 100
    query = "LIMIT 100 OFFSET {}".format(offset)
    return query


def select_all(table_name, special=None, spec_col=None, offset=None):
    # Build the SELECT query using the provided table name and optional special clause and/or specific columns
    query = build_query(table_name, spec_col, special)
    if offset is not None:
        query += " "
        query += add_offset(offset)
    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        # Fetch all rows from the query and returns them
        return cursor.fetchall()


def where_build(where_cols, like_cols=None):
    if not like_cols:
        like_cols = []
    # Calculate the number of items in the where list
    amount = len(where_cols)
    # Initialize the WHERE clause of the query
    query = " WHERE"
    # Iterate through the where list
    for i in range(amount):
        # Add the current item to the query
        query += " {}".format(where_cols[i])
        # Add a placeholder for the value of the current item
        if where_cols[i] == 'TimestampCreated':
            query += " = {} ".format('NOW()')
        elif not where_cols[i] in like_cols:
            query += " = %s "
        else:
            query += " LIKE %s "
        # If this is not the last item in the list, add AND
        if i < amount - 1:
            query += "AND"
    # Return the constructed WHERE clause
    return query


def select_spec(table_name, where_cols, what_to_find, spec_col=None, like_cols=None, offset=None):
    # Build the SELECT query using the provided table name and specific columns
    query = build_query(table_name, spec_col)
    # Append the WHERE clause to the SELECT query using the provided where_cols
    query += where_build(where_cols, like_cols=like_cols)
    # If offset is provided append the offset to the query
    if offset is not None:
        query += add_offset(offset)
    # Execute the query and return the result
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)
        return cursor.fetchall()


def select_spec_join(table1, table2, table1_col, table2_col, where_cols, what_to_find, spec_col=None, offset=None,
                     table3=None, table3_col=None, table1_col2=None):
    # Build the SELECT query using the provided table name and specific columns
    query = build_query(table1, spec_col)
    # Append the INNER JOIN clause to the SELECT query using the provided table2 and join conditions
    query += " INNER JOIN {}".format(table2)
    query += " ON {}".format(table1)
    query += ".{}".format(table1_col)
    query += " = {}".format(table2)
    query += ".{}".format(table2_col)
    # If table3 and join conditions are provided, append the additional join to the query
    if table3 is not None:
        query += " INNER JOIN {}".format(table3)
        query += " ON {}".format(table1)
        query += ".{}".format(table1_col2)
        query += " = {}".format(table3)
        query += ".{}".format(table3_col)
    # Append the WHERE clause to the SELECT query using the provided where_cols
    query += where_build(where_cols)
    # If offset is provided append the offset to the query
    if offset is not None:
        #
        query += add_offset(offset)
    # Execute the query and return the result
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)
        return cursor.fetchall()


def insert(table_name, columns, values):
    query = "INSERT INTO {} ".format(table_name)
    query += "("
    timestamp = False
    for column in columns:
        query += "{}, ".format(column)
        if column == "TimestampCreated":
            timestamp = True
    query = query[:-2]
    query += ") VALUES ("
    for value in values:
        query += "%s, "
    if timestamp:
        query += "{}, ".format("NOW()")
    query = query[:-2]
    query += ")"
    with connection.cursor() as cursor:
        cursor.execute(query, values)


def update(table_name, set_cols, updated_val, where_cols, what_to_find):
    # Build the UPDATE query using the provided table name and SET clause
    query = "UPDATE {} SET".format(table_name)
    for col in set_cols:
        query += " {} = %s,".format(col)
    query = query[:-1]
    # Append the WHERE clause to the UPDATE query using the provided where_cols
    query += where_build(where_cols)
    # Combine the updated values and what_to_find values for the execute statement
    updated_val += what_to_find
    # Execute the query with the provided values
    with connection.cursor() as cursor:
        cursor.execute(query, updated_val)


def delete(table_name, where_cols, what_to_find):
    # Build the DELETE query using the provided table name
    query = "DELETE FROM {}".format(table_name)
    # Append the WHERE clause to the DELETE query using the provided where_cols
    query += where_build(where_cols)
    # Execute the query with the provided values
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)


def count(table_name, where_cols, what_to_find):
    # Build the SELECT COUNT() query using the provided table name
    query = "SELECT Count(*) FROM {}".format(table_name)
    # Append the WHERE clause to the SELECT query using the provided where_cols
    query += where_build(where_cols)
    # Execute the query and return the first value of the result (the count)
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)
        return cursor.fetchone()[0]


def popular_sort_build(where_cols=None, offset=None, user=None):
    if where_cols is None:
        where_cols = []
    query = "SELECT p.id, p.TimestampCreated, p.Content, p.Title, game.Name, user.UserName, p.post_likes FROM "
    query += "(SELECT post.*, COUNT(likes.id) AS post_likes "
    query += "FROM post "
    # Add a JOIN clause to filter the posts by the user's games
    if user:
        query += "INNER JOIN usergames ug ON ug.Game_id = post.Game_id AND ug.User_id = %s "
    query += "LEFT JOIN likes ON likes.Post_id = post.Id "
    # Tried to send by days, but disabled for the moment, left here in case we fix the bug.
    # query += "WHERE post.TimestampCreated >= NOW() "
    # query += "- INTERVAL {} DAY ".format(day + 1)
    # query += "AND post.TimestampCreated < NOW() "
    # query += "- INTERVAL {} DAY ".format(day)
    for col in where_cols:
        query += "AND {}".format(col)
        query += " = %({}".format(col)
        query += ")s "
    query += "GROUP BY post.Id "
    query += ") AS p "
    query += "INNER JOIN game ON game.id = p.Game_id "
    query += "INNER JOIN user ON user.id = p.User_id "
    query += "ORDER BY p.post_likes DESC "
    if offset is not None:
        query += add_offset(offset)
    return query



def select_recent_game(game, offset=None):
    game_col = "post.Game_id"
    query = popular_sort_build(where_cols=[game_col], offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query, params={game_col: game})
        return cursor.fetchall()


def select_recent(offset=None):
    query = popular_sort_build(offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def select_recent_user(user_name, offset=None):
    query = popular_sort_build(offset=offset, user=user_name)
    with connection.cursor() as cursor:
        cursor.execute(query, [user_name])
        return cursor.fetchall()
