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
    offset *= 10
    query = "LIMIT 10 OFFSET {}".format(offset)
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
    with connection.cursor() as cursor:
        # Build the SELECT query using the provided table name and optional special clause and/or specific columns
        query = build_query(table_name, spec_col, special)
        if offset:
            query += add_offset(offset)
        # Execute the query
        cursor.execute(query)
        # Fetch all rows from the query and returns them
        return cursor.fetchall()


def where_build(where_cols):
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
            query += " = {}".format('NOW()')
        else:
            query += " = %s"
        # If this is not the last item in the list, add AND
        if i < amount - 1:
            query += " AND"
    # Return the constructed WHERE clause
    return query


def select_spec(table_name, where_cols, what_to_find, spec_col=None):
    with connection.cursor() as cursor:
        query = build_query(table_name, spec_col)
        query += where_build(where_cols)
        cursor.execute(query, what_to_find)
        return cursor.fetchall()


def select_spec_join(table1, table2, table1_col, table2_col, where_cols, what_to_find, spec_col=None):
    with connection.cursor() as cursor:
        query = build_query(table1, spec_col)
        query += " INNER JOIN {}".format(table2)
        query += " ON {}".format(table1)
        query += ".{}".format(table1_col)
        query += " = {}".format(table2)
        query += ".{}".format(table2_col)
        query += where_build(where_cols)
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


def popular_sort_build(where_cols=None, offset=None):
    if where_cols is None:
        where_cols = []
    query = "SELECT * FROM "
    query += "(SELECT post.*, COUNT(likes.id) AS post_likes "
    query += "FROM post "
    query += "LEFT JOIN likes ON likes.PostId_id = post.Id "
    query += "WHERE post.TimestampCreated >= NOW() - INTERVAL 1 DAY "
    for col in where_cols:
        query += "AND {}".format(where_cols)
        query += " = %({)".format(where_cols)
        query += ")s "
    query += "GROUP BY post.Id "
    query += ") AS p "
    query += "ORDER BY p.post_likes DESC "
    if offset:
        query += add_offset(offset)
    return query



def select_recent_game(game, offset=None):
    game_col = "post.GameName_id"
    query = popular_sort_build([game_col], offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query, params={game_col: game})
        return cursor.fetchall()


def select_recent(offset=None):
    query = popular_sort_build(offset=offset)
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
