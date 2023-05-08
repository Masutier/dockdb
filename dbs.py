import json
import mariadb
import pymongo

with open("/home/gabriel/prog/json_config/connmaria.json") as config_file:
    sec_config = json.load(config_file)


def conn_mariadb():
    conn = mariadb.connect (
        host= '127.0.0.1',
        port= int(sec_config["MARIADB_PORT"]),
        user= sec_config["MARIADB_USER"],
        password= sec_config["MARIADB_PASSWORD"],
        database= 'testing')

    return conn


def conn_mongodb():
    mongoclient = pymongo.MongoClient(sec_config["MONGODB_PORT"])

    return mongoclient
