import interface.back.connector


def add_func():
    connection = interface.back.connector.create_connection("localhost", "root", "root", "Metadata")
    cursor = connection.cursor()

    insert = """ insert into db
              (name)
            values (%s)"""
    tables = ("LoL")
    data = (tables,)
    cursor.execute(insert, data)

    connection.commit()
    cursor.close()
    connection.close()
