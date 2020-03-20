from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import blockchainSetup
from blockchainSetup import  web3

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


@app.route("/makeDonation", methods=['POST'])
def donate():
    charity = request.args.get("charityAddress")
    amount = request.args.get("amount")
    pid = request.args.get("projectId")
    donor = request.args.get("donorAddress")
    txn = blockchainSetup.make_donation(charity, amount, pid,donor)
    dic = {"txn": txn}
    return jsonify(dic)


@app.route("/registerInspector", methods=['POST'])
def registerInspector():
    # address = request.form.get("inspectorAddress")
    # print(address)
    address = request.args.get("inspectorAddress")
    # print(address)
    txn = blockchainSetup.registerInspector(address)
    dic = {"txn": txn}
    return jsonify(dic)


@app.route("/registerDonor", methods=['POST'])
def registerDonor():
    address = request.args.get("donorAddress")
    print(address)
    # address1 = request.args.get("inspectorAddress")
    txn = blockchainSetup.registerDonor(address)
    dic = {"txn": txn}
    return jsonify(dic)


@app.route("/approveDonor", methods=['POST'])
def approveDonor():
    donor = request.args.get("donorAddress")
    inspector = request.args.get("inspectorAddress")
    print(donor)
    print(inspector)
    txn = blockchainSetup.approveDonor(donor, inspector)
    dic = {"txn":txn}
    return jsonify(dic)

@app.route("/registerOrganization", methods=['POST'])
def registerOrganization():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.registerOrganization(charity)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/approveOrganization", methods=['POST'])
def approveOrganization():
    charity = request.args.get("charityAddress")
    inspector = request.args.get("inspectorAddress")
    print(charity)
    print(inspector)
    txn = blockchainSetup.approveOrganization(charity, inspector)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/rejectOrganization", methods=['POST'])
def rejectOrganization():
    charity = request.args.get("charityAddress")
    inspector = request.args.get("inspectorAddress")
    print(charity)
    print(inspector)
    txn = blockchainSetup.rejectOrganization(charity, inspector)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/updateOrganization", methods=['POST'])
def updateOrganization():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.updateOrganization(charity)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/deleteOrganization", methods=['DELETE'])
def deleteOrganization():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.deleteOrganization(charity)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/approvedOrganization", methods=['GET'])
def approvedOrganization():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.approvedOrganization(charity)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/getOrganizationName", methods=['GET'])
def getOrganizationName():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.getOrganizationName(charity)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/confirmReceiveMoney", methods=['POST'])
def confirmReceiveMoney():
    donation = request.args.get("donationId")
    inspector = request.args.get("inspectorAddress")
    print(donation)
    txn = blockchainSetup.confirmReceiveMoney(donation, inspector)
    dic = {"txn": txn}
    return jsonify(dic)

if __name__ == "__main__":
    app.run(debug=True)


