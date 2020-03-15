from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import blockchainSetup 

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

@app.route("/registerDonor", methods=['POST'])
def rigisterDonor():
    email = request.form["email"]
    password = request.form["password"]
    # TODO: complete rigiester donor code

    return jsonify(200)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/makeDonation", methods=['POST'])
def donate():
    charity = request.form["charityAddress"]
    amount = request.form["amount"]
    return blockchainSetup.makeDonation(charity,amount)
