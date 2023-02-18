import connector


def add_func():
    connection = connector.create_connection("localhost", "root", "root", "MetaData")
    cursor = connection.cursor()

    insert = """ insert into servers
              (adress, userName, passwd, namen, portnum)
            values (%s, %s, %s, %s, %s, %s)"""
    server = ("localhost", "root", "root", "OCE", "3306")
    for k in server:
        data = (k,)
        cursor.execute(insert, data)

    connection.commit()
    cursor.close()
    connection.close()