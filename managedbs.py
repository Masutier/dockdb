import os
import json
import mariadb
import pymongo
import flask
from flask import Flask, render_template as render, redirect
from maria import insertMariadb, extractMariadb
from mongo import connMongodb, extractMongodb
from bson.objectid import ObjectId


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
with open("/home/gabriel/prog/json_config/connmaria.json") as config_file:
    sec_config = json.load(config_file)

# create the flask app
app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']

mydict = { "name": "Oliver", "address": "Costal Rd 1427" }
mylist = [
    { "name": "Eliot", "address": "esmerald Rd 5554"},
    { "name": "Josefine", "address": "River Rd 4235"},
    { "name": "Stephany", "address": "Coral Dr 3256"},
    { "name": "Alice", "address": "Wonderland Av 1589"},
    { "name": "Jaqueline", "address": "Castle View 8745"},
    { "name": "Coco", "address": "Beverly Hills 55544"},
]


@app.route('/')
def home():
    return render('home.html', title="DataBases")


# MARIADB
@app.route('/homeMariadb')
def homeMariadb():
    data = []
    data = extractMariadb()

    return render('homeMaria.html', title="Mariadb", data=data)


@app.route('/insertPeopleMdb', methods=['GET'])
def insertPeopleMdb():
    data = []
    insertMariadb(mylist)
    data = extractMariadb()

    return render('people.html', title="Mariadb", data=data)


# MONGODB
@app.route('/homeMongodb')
def homeMongodb():
    data = []
    data = extractMongodb()

    return render('homeMongo.html', title="Mongodb", data=data)


@app.route('/insertMongodb', methods=['GET'])
def insertMongodb():
    data = []
    dbColl = connMongodb()
    #x = dbColl.insert_one(mydict)    # ==>> Insert only one person, see on top of the code 
    x = dbColl.insert_many(mylist)     # ==>> Insert a list, see on top of the code
    data = extractMongodb()

    return render('seecust.html', title="Mongodb", data=data)


@app.route('/deleteRecordMongodb/<pk>', methods=['GET', 'POST'])
def deleteRecordMongodb(pk):
    dbColl = connMongodb()
    x = dbColl.delete_one({'_id': ObjectId(pk)})

    return redirect('/homeMongodb')


# run the app
app.run(debug=True)
