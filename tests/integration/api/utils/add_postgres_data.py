from grpc_test_server.users_data import users, users_data
from psycopg import Cursor


def add_users(cur: Cursor) -> None:
    sql = """
    INSERT INTO users_auth.users(id, login, password)
    VALUES(%s, %s, %s)
    """
    cur.executemany(sql, users)
    cur.connection.commit()

    sql = """
    INSERT INTO users_auth.users_data(user_id, email)
    VALUES(%s, %s)
    """
    cur.executemany(sql, users_data)
    cur.connection.commit()
