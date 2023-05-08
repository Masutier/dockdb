import json
import mariadb
import pymongo
from dbs import conn_mariadb


def insertMariadb(mylist):
    conn = conn_mariadb()

    for result in mylist:
        name = result['name']
        address = result['address']
        sqlQuery = f"""INSERT INTO people VALUES (
                '{name}',
                '{address}'
            )"""
        cursor = conn.cursor()
        cursor.execute(sqlQuery)
    conn.commit()

    return


def extractMariadb():

    conn = conn_mariadb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")  # execute a SQL statement

    headers=[x[0] for x in cursor.description]      # serialize results into JSON
    allData = cursor.fetchall()
    data = [] 

    for result in allData:
        data.append(dict(zip(headers,result)))

    return data
