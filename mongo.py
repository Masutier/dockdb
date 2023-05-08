import json
import pymongo
from dbs import conn_mongodb


def connMongodb():
    mongoclient = conn_mongodb()
    dbase = mongoclient["mongodbase"]
    dbColl = dbase["customers"]

    return dbColl


def extractMongodb():
    mongoclient = conn_mongodb()
    dbase = mongoclient["mongodbase"]
    dbColl = dbase["customers"]
    data=[] 

    for result in dbColl.find():
        data.append(result)

    return data


