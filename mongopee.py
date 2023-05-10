import os
import json
import pymongo
import flask
import pandas as pd
from flask import Flask, render_template as render, redirect, jsonify
from peewee import *
from pymongo import MongoClient


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
with open("/home/gabriel/prog/json_config/connmaria.json") as config_file:
    sec_config = json.load(config_file)

# create the flask app
app = Flask(__name__, static_url_path='/static')
app.secret_key = sec_config['SECRET_KEY']

destiny_path = "/home/gabriel/prog/cleanCsvFlask/docs/"
origen_path = "/home/gabriel/Downloads/"

conn = MongoClient("mongodb://localhost:27017/")

@app.route('/')
def home():
    db = conn['Neptuno']
    dataAll = []
    categories = db.Categorias.find()
    for category in categories:
        dataAll.append({
                "Idcategoria":category["Idcategoria"],
                "Nombrecategoria":category["Nombrecategoria"],
                "Descripcion":category["Descripcion"]
            })
    data = dataAll
    return render('home2.html', title="Mongodb", data=data)


# MONGODB
@app.route('/mongoPee')
def mongoPee():
    db = conn['Neptuno']
    excFile = pd.read_excel(origen_path + "Neptuno.xlsx", sheet_name="2,-Categorias")
    data = []
    dataAll = []
    for item in excFile:
        data.append(item)
    
    z0 = excFile[data[0]]
    z1 = excFile[data[1]]
    z2 = excFile[data[2]]
    j = len(excFile)

    #INSERT TO DB
    count = 0
    while count < j:
        db.Categorias.insert_one({
            "Idcategoria":int(z0[count]),
            "Nombrecategoria":z1[count],
            "Descripcion":z1[count]
        })
        count += 1
    
    #DISPLAY
    categories = db.Categorias.find()
    for category in categories:
        dataAll.append({
                "Idcategoria":category["Idcategoria"],
                "Nombrecategoria":category["Nombrecategoria"],
                "Descripcion":category["Descripcion"]
            })
    data = dataAll

    return render('homeMongo2.html', title="Mongodb", data=data)






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
