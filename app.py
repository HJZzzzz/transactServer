from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import blockchainSetup
from blockchainSetup import  web3
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
title = "TransACT Server"
CORS(app)

client = MongoClient('localhost', 27017)
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

    donor_id = ''
    try:
        txn = blockchainSetup.registerDonor(request.form.get("eth_address"))
        new_donor = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "email": request.form.get("email"),
            "eth_address": request.form.get("eth_address"),
            "bank_account": request.form.get("bank_account"),
            "physical_address": request.form.get("physical_address"),
            "full_name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
            "financial_info": request.form.get("financial_info"),
            "registration_hash": txn,
            "approval_hash": ''
        }
        donor_id = db.donors.insert_one(new_donor)

    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"error": str(ex)}
            # {"error": str(ex.args[0]['message'])}
        )

    print(donor_id)
    # dic = {"donor_id": str(donor_id.inserted_id)}
    # return jsonify(dic)
    return jsonify(200)


@app.route("/approveDonor", methods=['POST'])
def approveDonor():
    donors = db.donors

    donor = request.args.get("donorAddress")
    inspector = request.args.get("inspectorAddress")

    try:
        txn = blockchainSetup.approveDonor(donor, inspector)

        result = donors.find_one_and_update(
            {"eth_address": donor},
            {"$set":{
                "approval_hash":txn
            }
             },upsert=True
        )
        # dic = {"txn": txn}
        return jsonify(200)
    except Exception as ex:
        return jsonify({"error":str(ex)})


@app.route("/registerOrganization", methods=['POST'])
def registerOrganization():

    charity = request.form.get("charityAddress")

    try:

        txn = blockchainSetup.registerOrganization(charity)
        new_charity = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "email": request.form.get("email"),
            "eth_address": request.form.get("eth_address"),
            "bank_account": request.form.get("bank_account"),
            "physical_address": request.form.get("physical_address"),
            "name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
            "financial_info": request.form.get("financial_info"),
            "description": request.form.get("description"),
            "registration_hash": txn,
            "approval_hash":''
        }
        charity_id = db.donors.insert_one(new_charity)
    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"error": str(ex)}
            # {"error": str(ex.args[0]['message'])}
        )

    # dic = {"charity_id": str(charity_id.inserted_id)}
    # return jsonify(dic)
    return jsonify(200)


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


@app.route("/registerProject", methods=['POST'])
def registerProject():
    charity = request.args.get("charityAddress")
    beneficiaryListId = request.args.get('beneficiaryListId')
    documentationId = request.args.get('documentationId')
    beneficiaryGainedRatio = request.args.get('beneficiaryGainedRatio')
    
    txn = blockchainSetup.registerProject(charity, beneficiaryListId, documentationId, beneficiaryGainedRatio)
    dic = {"txn": txn}
    return jsonify(dic)


@app.route("/approveProject", methods=['POST'])
def approveProject():
    project = request.args.get('projectId')
    inspector = request.args.get('inspectorAddress')
    txn = blockchainSetup.approveProject(inspector, project)
    dic = {"txn": txn}
    return jsonify(dic)


@app.route("/rejectProject", methods=['POST'])
def rejectProject():
    project = request.args.get('projectId')
    inspector = request.args.get('inspectorAddress')
    txn = blockchainSetup.rejectProject(inspector, project)
    dic = {"txn": txn}
    return jsonify(dic)

@app.route("/donor/login", methods=['GET'])
def loginDonor():
    donors = db.donors
    try:
        results = donors.find_one({"username": request.args.get("username")})
        print(results)
        print(":::")
        if ( len(results) and results["password"] == request.args.get("password")):
            print(results["approval_hash"])
            print("::")
            approval = blockchainSetup.checkDonorApproval(results["approval_hash"])
            print(approval)
            print(":")
            if(approval):
                return jsonify(
                    {"id": str(results["_id"]),
                     "username": results["username"],
                     "eth_address": results["eth_address"]
                     }
                )
            else:
                return jsonify({"error": "Your account is still waiting for approval!"})

        else:
            return jsonify({"error": "username or password not correct"})

    except Exception as ex:
        # print(ex)
        # print(type(ex))
        return jsonify(
            {"error": "username or password not correct"}
        )


@app.route("/charity/login", methods=['GET'])
def loginCharity():
    charites = db.donors
    try:
        results = charites.find_one({"username": request.args.get("username")})
        print(results)
        if ( len(results) and results["password"] == request.args.get("password")):
            return jsonify(
                {"id": str(results["_id"]),
                 "username": results["username"],
                 "eth_address": results["eth_address"]
                 }
            )
        else:
            return jsonify({"error": "username or password not correct"})
    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"error": "username or password not correct"}
        )


@app.route("/admin/login", methods=['GET'])
def loginAdmin():
    if(
        request.args.get("password") == "admin"
        and
        request.args.get("username") == "admin"
    ):
        return jsonify(200)

    return jsonify(
            {"error": "username or password not correct"}
        )


if __name__ == "__main__":
    app.run(debug=True)


