from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
title = "TransACT Server"
CORS(app)

client = MongoClient("mongodb+srv://transactAdmin:transact@transact-tsjmg.mongodb.net/test?retryWrites=true&w=majority")
db = client['transact']

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test", methods=['GET'])
def testGet():
    dic = {"value": 1}
    return jsonify(dic)

@app.route("/charity/register", methods=['POST'])
def registerDonor():
    charity = db.charity
    try:
        charity.insert_one({
            "email":request.form["email"], 
            "password":request.form["password"],
            "username": request.form["username"],
            "region": request.form["region"]
        })
        
    except e:
        print(e)

    return jsonify(200)

@app.route("/donor/login", methods=['GET'])
def loginDonor():
    donors = db.donors
    try:
        results = donors.find_one({"_id": ObjectId("5e7611d5d594a75088cec8d1")})
        results["_id"] = str(results["_id"])
        print(results)
    except:
        print("error")

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)