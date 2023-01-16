from django.db import connection


def build_query(table_name, columns, special=None):
    """
    Build a SELECT query for a given table.

    Parameters:
        table_name (str): The name of the table to select from.
        columns (List[str]): The list of columns to select. If None, all columns are selected.
        special (str): An optional string to add to the SELECT clause.

    Returns:
        str: The constructed SELECT query.
    """
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
    offset *= 100
    query = "LIMIT 100 OFFSET {}".format(offset)
    return query


def select_all(table_name, special=None, spec_col=None, offset=None):
    """
    Executes a SELECT * FROM table_name query with the option to include a special clause (such as DISTINCT or LIMIT)
    and/or select specific columns.

    Parameters:
        table_name (str): The name of the table to query.
        special (str, optional): A special clause to include in the query (default is None).
        spec_col (list, optional): A list of specific columns to select (default is None).
        offset (int, optional): an offset to start from
    Returns:
        list: A list of tuples, where each tuple represents a row in the table.
    """

    # Build the SELECT query using the provided table name and optional special clause and/or specific columns
    query = build_query(table_name, spec_col, special)
    if offset:
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
    query = build_query(table_name, spec_col)
    query += where_build(where_cols, like_cols=like_cols)
    if offset is not None:
        query += add_offset(offset)
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)
        return cursor.fetchall()


def select_spec_join(table1, table2, table1_col, table2_col, where_cols, what_to_find, spec_col=None, offset=None,
                     table3=None, table3_col=None, table1_col2=None):
    query = build_query(table1, spec_col)
    query += " INNER JOIN {}".format(table2)
    query += " ON {}".format(table1)
    query += ".{}".format(table1_col)
    query += " = {}".format(table2)
    query += ".{}".format(table2_col)
    if table3 is not None:
        query += " INNER JOIN {}".format(table3)
        query += " ON {}".format(table1)
        query += ".{}".format(table1_col2)
        query += " = {}".format(table3)
        query += ".{}".format(table3_col)
    query += where_build(where_cols)
    if offset is not None:
        #
        query += add_offset(offset)
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
    query = "UPDATE {} SET".format(table_name)
    for col in set_cols:
        query += " {} = %s,".format(col)
    query = query[:-1]
    query += where_build(where_cols)
    updated_val += what_to_find
    with connection.cursor() as cursor:
        cursor.execute(query, updated_val)


def delete(table_name, where_cols, what_to_find):
    query = "DELETE FROM {}".format(table_name)
    query += where_build(where_cols)
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)


def count(table_name, where_cols, what_to_find):
    query = "SELECT Count(*) FROM {}".format(table_name)
    query += where_build(where_cols)
    with connection.cursor() as cursor:
        cursor.execute(query, what_to_find)
        return cursor.fetchone()[0]


def popular_sort_build(day, where_cols=None, offset=None, user=None):
    if where_cols is None:
        where_cols = []
    query = "SELECT p.id, p.TimestampCreated, p.Content, p.Title, game.Name, user.UserName, p.post_likes FROM "
    query += "(SELECT post.*, COUNT(likes.id) AS post_likes "
    query += "FROM post "
    if user:
        query += "INNER JOIN usergames ug ON ug.Game_id = post.Game_id AND ug.User_id = %s "
    query += "LEFT JOIN likes ON likes.Post_id = post.Id "
    query += "WHERE post.TimestampCreated >= NOW() "
    query += "- INTERVAL {} DAY ".format(day + 1)
    query += "AND post.TimestampCreated < NOW() "
    query += "- INTERVAL {} DAY ".format(day)
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



def select_recent_game(day, game, offset=None):
    game_col = "post.Game_id"
    query = popular_sort_build(day, where_cols=[game_col], offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query, params={game_col: game})
        return cursor.fetchall()


def select_recent(day, offset=None):
    query = popular_sort_build(day, offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def select_recent_user(user_name, day, offset=None):
    query = popular_sort_build(day, offset=offset, user=user_name)
    with connection.cursor() as cursor:
        cursor.execute(query, [user_name])
        return cursor.fetchall()
