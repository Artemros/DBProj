import interface.back.connector


def add_func():
    connection = interface.back.connector.create_connection("localhost", "root", "root", "Metadata")
    cursor = connection.cursor()

    insert = """ insert into tablename
              (name)
            values (%s)"""
    tables = ("assistants", "champion", "characteristic_of_game", "current_statistics", "inventory", "items", "killing",
              "mastery", "matches", "player", "ranking", "server", "slot", "statistics_log", "view1")
    for k in tables:
        data = (k,)
        cursor.execute(insert, data)

    connection.commit()
    cursor.close()
    connection.close()
