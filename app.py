from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import blockchainSetup
import datetime
from blockchainSetup import  web3
from pymongo.errors import ConnectionFailure
from bson.json_util import dumps
import os
import hashlib
import pandas as pd
from pathlib import Path
import copy
import io
import base64
from PIL import Image


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
    try:
        amount = request.form.get("amount")
        pid = request.form.get("project_id")
        donor = request.form.get("donor_id")
        result = db.donors.find_one({"_id": ObjectId(donor)})
        result1 = db.projects.find_one({"_id": ObjectId(pid)})
        anonymous = request.form.get("anonymous")
        # To protect user privacy, we will use sha256 to hash the donor' eth address
        txn = blockchainSetup.make_donation(int(amount), int(result1['project_solidity_id']), result['eth_address'])
        print(txn)
        new_donation = {
            "amount": amount,
            "project_id": ObjectId(pid),
            "donor_id": ObjectId(donor),
            "donor_address": request.form.get("donor_address"),
            "donation_time": str(datetime.datetime.now().strftime("%Y-%m-%d")),
            "donation_hash": txn,
            "anonymous": anonymous
        }

        donation_id = db.donations.insert_one(new_donation)
        return jsonify({'code': 200})
    
    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"code": 400,
            "error": str(ex)}
        )




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
        address = request.form.get("eth_address")
        
        unique_username = db.donors.find_one({'username': request.form.get("username")})
        unique_eth_add = db.donors.find_one({'eth_address': request.form.get("eth_address")})
        if unique_username is not None:
            return jsonify({
                "code":400,
                "message": 'This username has been taken, please try another one'})
        if unique_eth_add is not None:
            return jsonify({
                "code":400,
                "message": 'This ethereum address already has an account'})
                
        txn = blockchainSetup.registerDonor(address, request.form.get("full_name"))

        #hash password
        salt = os.urandom(32)
        password = request.form.get("password")
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        # Store them as:
        passwordStorage = salt + key

        new_donor = {
            "username": request.form.get("username"),
            "password": passwordStorage,
            "email": request.form.get("email"),
            "eth_address": request.form.get("eth_address"),
            "card_number": request.form.get("card_number"),
            "card_expiry_date": request.form.get("card_expiry_date"),
            "physical_address": request.form.get("physical_address"),
            "full_name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
            "financial_info": request.form.get("financial_info"),
            "registration_hash": txn,
            "approval_hash": ''
        }
        donor_id = db.donors.insert_one(new_donor)

    except Exception as ex:
        if(str(type(ex)) == "<class 'web3.exceptions.InvalidAddress'>"):
            return jsonify(
                {
                    "code": 400,
                    "message": "Invalid Eth Address"
                }
            )

        return jsonify(
            {
                "code":400,
                "message": str(ex)
            }
            # {"error": str(ex.args[0]['message'])}
        )

    return jsonify({"code":200})

@app.route("/updateDonor", methods=['POST'])
def updateDonor():

    donors = db.donors
    donor = request.form.get("eth_address")

    try:
        txn = blockchainSetup.updateDonor(donor, request.form.get("full_name"))
        updateDic = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "card_number": request.form.get("card_number"),
            "card_expiry_date": request.form.get("card_expiry_date"),
            "physical_address": request.form.get("physical_address"),
            "full_name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
        }

        if "password" in request.form:
            password = request.form.get("password")
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            passwordStorage = salt + key
            updateDic["password"] = passwordStorage

        result = donors.find_one_and_update(
            {"eth_address": donor},
            {"$set": updateDic
            }
        )
        dic = {"code": 200}
        return jsonify(dic)
    except Exception as ex:
        return jsonify({"error":str(ex)})

@app.route("/approveDonor", methods=['POST'])
def approveDonor():
    donors = db.donors

    donor = request.form.get("donorAddress")
    inspector = request.form.get("inspectorAddress")

    try:
        txn = blockchainSetup.approveDonor(donor, inspector)

        result = donors.find_one_and_update(
            {"eth_address": donor},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        # dic = {"txn": txn}
        return jsonify({
                "code":200,
                "message": "Approve Donor"
            })
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/rejectDonor", methods=['POST'])
def rejectDonor():
    donors = db.donors

    donor = request.form.get("donorAddress")
    inspector = request.form.get("inspectorAddress")

    try:
        txn = blockchainSetup.rejectDonor(donor, inspector)

        result = donors.find_one_and_update(
            {"eth_address": donor},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        return jsonify({
                "code":200,
                "message": "Reject Donor"
            })
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/getDonorDetails", methods=['GET'])
def getDonorDetails():
    donor = request.args.get("donorAddress")
    print(donor)

    try: 
        # txn = blockchainSetup.getDonorDetails(donor)
        db_result = db.donors.find_one({"eth_address":donor})
        db_result['_id'] = str(db_result['_id'])
        db_result['password'] = ""
        db_result["code"] = "200"
        return jsonify(db_result)
        
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/getAllDonors", methods=['GET'])
def getAllDonors():
    try: 
        db_result = db.donors.find()
        result_list = []
        for result in db_result:
            result['_id'] = str(result['_id'])
            print(result)
            result_list.append(result)

        return jsonify(
            {"code": 200,
            "items": result_list}
        )
        
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/getAllPendingDonors", methods=['GET'])
def getAllPendingDonors():
    try:
        db_result = db.donors
        result_list = []
        all_result = db_result.find(
            {"approval_hash": ''}
        )
        for result in all_result:
            result['_id'] = str(result['_id'])
            result['password'] = ""
            result_list.append(result)

        return jsonify(
            {"code": 200,
            "items": result_list}
        )
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })
            
# @app.route("/getDonorsByProject", methods=['GET'])
# def getDonorsByProject():
#     projectId = request.args.get("projectId")
#     print(projectId)
#     try:
#         db_result = db.donations.find({"project_id":projectId})
#         dic = {"code":200}
#         i = 0
#         for result in db_result:
#             donor = result['donor_address']
#             donor_details = db.donors.find_one({"eth_address":donor})
#             donor_details['_id'] = str(donor_details['_id'])
#             print(donor_details)
#             dic[str(i)]=donor_details
#             i+=1
#         dic["message"]=i
#         return jsonify(dic)
#
#     except Exception as ex:
#         return jsonify({
#                 "code":400,
#                 "message": str(ex)
#             })

@app.route("/getProjectsByOrganization", methods=['GET'])
def getProjectsByOrganization():
    charity = request.args.get("charityAddress")
    try:
        db_result = db.projects.find({"charityAddress":charity})
        result_list = []
        for result in db_result:         
            donations = list(db.donations.find({"project_id": ObjectId(result['_id'])}))
            num = 0
            numDonors = 0

            stop = blockchainSetup.checkProjectStop(result['approval_hash'], result['project_solidity_id'])
            aproval = blockchainSetup.checkProjectApproval(result['approval_hash'], result['project_solidity_id'])
            reject =  blockchainSetup.checkProjectReject(result['approval_hash'], result['project_solidity_id'])
            if(stop):
                result['stop'] = "1"        #project stopped
            elif(reject):
                result['stop'] = "10"   #rejected
            elif(aproval):           # approved
                result['stop'] = "0"
            else:     #wait approval
                result['stop'] = '-1'


            for d in donations:
                num += int(d['amount'])
                numDonors += 1

            confirmations = list(db.confirmations.find({"project_id":ObjectId(result['_id'])}))
            total_confirm = 0
            for c in confirmations:
                total_confirm += int(c['amount'])

            result['actual_amount'] = num
            result['confirmed_amount'] = total_confirm
            result['num_donors'] = numDonors
            result['_id'] = str(result['_id'])
            result['charity_id'] = str(result['charity_id'])
            result_list.append(result)
        dic = {"code":200, "items":result_list}    
        return jsonify(dic)
        
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })     

@app.route("/getProjectsByDonor", methods=['GET'])
def getProjectsByDonor():
    donor = request.args.get("donorAddress")
    print(donor)
    try: 
        donation_result = db.donations.find({"donor_address":donor})
        unique_projects = list(set([ str(result["project_id"]) for result in donation_result]))

        result_list = []
        for project_id in unique_projects:
            project = db.projects.find_one({"_id":ObjectId(project_id)})

            donations = list(db.donations.find({"project_id": ObjectId(project_id)}))
            self_donations = list(db.donations.find({
                "project_id": ObjectId(project_id),
                "donor_address": donor
            }))
            result = {}
            result['_id'] = project_id


            stop = blockchainSetup.checkProjectStop(project['approval_hash'], project['project_solidity_id'])
            if(stop):
               result['stop'] = "1"
            elif(result['approval_hash']==''):
               result['stop'] = '-1'
            else:
               result['stop'] = "0"

            num = 0
            for d in donations:
                num += int(d['amount'])
            # total amount: $$ of donations
            confirmations = list(db.confirmations.find({"project_id":ObjectId(project_id)}))
            total_confirm = 0
            for c in confirmations:
                total_confirm += int(c['amount'])

            totl_contributed = 0
            for s in self_donations:
                totl_contributed += int(s["amount"])

            result['actual_amount'] = num
            result['confirmed_amount'] = total_confirm
            result['amount'] = totl_contributed
            result['projectName'] = project['projectName']
            result['expirationDate'] = project['expirationDate']
            result['fundTarget'] = project['fundTarget']

            result_list.append(result)  
        dic = {"code":200, "items":result_list}    
        return jsonify(dic)
        
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })                         


@app.route("/registerOrganization", methods=['POST'])
def registerOrganization():

    charity = request.form.get("eth_address")
    try:
        unique_username = db.charities.find_one({'username': request.form.get("username")})
        unique_eth_add = db.charities.find_one({'eth_address': request.form.get("eth_address")})
        if unique_username is not None:
            return jsonify({
                "code":400,
                "message": 'This username has been taken, please try another one'})
        if unique_eth_add is not None:
            return jsonify({
                "code":400,
                "message": 'This ethereum address already has an account'})
        
        txn = blockchainSetup.registerOrganization(charity, request.form.get("full_name"))

        #hash password
        salt = os.urandom(32)
        password = request.form.get("password")
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        # Store them as:
        passwordStorage = salt + key

        new_charity = {
            "username": request.form.get("username"),
            "password": passwordStorage,
            "email": request.form.get("email"),
            "eth_address": request.form.get("eth_address"),
            "card_number": request.form.get("card_number"),
            "card_expiry_date": request.form.get("card_expiry_date"),
            "physical_address": request.form.get("physical_address"),
            "full_name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
            "description": request.form.get("description"),
            "registration_hash": txn,
            "approval_hash":''
        }
        charity_id = str(db.charities.insert_one(new_charity).inserted_id)
        
        #store certificate
        certificate = request.files["certificate"]
        folder_path = "./certificate/" + request.form.get("eth_address") + "/"
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        filename = "certificate.pdf"
        certificate.save(os.path.join(folder_path, filename))

    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"code": 400,
            "message": str(ex)}
            # {"error": str(ex.args[0]['message'])}
        )

    return jsonify({"code":200, "charity_id": charity_id})


@app.route("/approveOrganization", methods=['POST'])
def approveOrganization():

    charities = db.charities

    charity = request.form.get("charityAddress")
    inspector = request.form.get("inspectorAddress")

    try:
        txn = blockchainSetup.approveOrganization(charity, inspector)
        result = charities.find_one_and_update(
            {"eth_address": charity},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        # dic = {"txn": txn}
        return jsonify({
                "code": 200,
                "message": "Approve organization"
                })
    except Exception as ex:
        return jsonify({
                "code": 400,
                "message": str(ex)
                })


@app.route("/rejectOrganization", methods=['POST'])
def rejectOrganization():

    charities = db.charities

    charity = request.form.get("charityAddress")
    inspector = request.form.get("inspectorAddress")

    try:
        txn = blockchainSetup.rejectOrganization(charity, inspector)

        result = charities.find_one_and_update(
            {"eth_address": charity},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        # dic = {"txn": txn}
        return jsonify({
                "code": 200,
                "message": "Reject organization"
                })
    except Exception as ex:
        return jsonify({
                "code": 400,
                "message": str(ex)
                })


@app.route("/updateOrganization", methods=['POST'])
def updateOrganization():

    charities = db.charities
    charity = request.form.get("eth_address")

    try:
        txn = blockchainSetup.updateOrganization(charity, request.form.get("full_name"))
        updateDic = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "card_number": request.form.get("card_number"),
            "card_expiry_date": request.form.get("card_expiry_date"),
            "physical_address": request.form.get("physical_address"),
            "full_name": request.form.get("full_name"),
            "contact_number": request.form.get("contact_number"),
            "description": request.form.get("description"),
        }

        if "password" in request.form:
            password = request.form.get("password")
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            passwordStorage = salt + key
            updateDic["password"] = passwordStorage

        result = charities.find_one_and_update(
            {"eth_address": charity},
            {"$set": updateDic
            }
        )

        #update certificate
        if "certificate" in request.files:
            certificate = request.files["certificate"]
            folder_path = "./certificate/" + charity + "/"
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            filename = "certificate.pdf"
            certificate.save(os.path.join(folder_path, filename))

        dic = {"code": 200}
        return jsonify(dic)
    except Exception as ex:
        return jsonify({"error":str(ex)})


# @app.route("/deleteOrganization", methods=['DELETE'])
# def deleteOrganization():
#
#     charities = db.charities
#
#     charity = request.args.get("charityAddress")
#
#     try:
#         txn = blockchainSetup.deleteOrganization(charity)
#
#         result = charities.delete_one(
#             {"eth_address": charity}
#         )
#
#         return jsonify(200)
#     except Exception as ex:
#         return jsonify({"error":str(ex)})

@app.route("/getAllPendingOrganizations", methods=['GET'])
def getAllPendingOrganizations():
    try:
        db_result = db.charities
        result_list = []
        all_result = db_result.find(
            {"approval_hash": ''}
        )
        for result in all_result:
            result['_id'] = str(result['_id'])
            result['password'] = ""
            result_list.append(result)

        return jsonify(
            {"code": 200,
            "items": result_list}
        )
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })


@app.route("/approvedOrganization", methods=['GET'])
def approvedOrganization():
    charity = request.args.get("charityAddress")
    print(charity)
    txn = blockchainSetup.approvedOrganization(charity)
    dic = {"txn": txn}
    return jsonify(dic)


# @app.route("/getOrganizationName", methods=['GET'])
# def getOrganizationName():
#     charity = request.args.get("charityAddress")
#     print(charity)
#     txn = blockchainSetup.getOrganizationName(charity)
#     dic = {"txn": txn}
#     return jsonify(dic)

@app.route("/getCharityDetails", methods=['GET'])
def getCharityDetails():
    charity = request.args.get("charityAddress")
    print(charity)

    try: 
        db_result = db.charities.find_one({"eth_address":charity})
        db_result['_id'] = str(db_result['_id'])
        db_result["password"] = ""
        db_result["code"] = 200,
        return jsonify(db_result)
        
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })    

@app.route("/confirmMoney", methods=['POST'])
def confirmMoney():
    try:

        amount = request.form.get("amount")
        project_id = request.form.get("project_id")
        description = request.form.get("description")
        charity = request.form.get("charity_id")
        result = db.charities.find_one({"_id": ObjectId(charity)})
        result1 = db.projects.find_one({"_id": ObjectId(project_id)})

        txn = blockchainSetup.confirmMoney(int(amount), int(result1['project_solidity_id']), result['eth_address'])
        new_confirmation = {
            "amount": amount,
            "project_id": ObjectId(project_id),
            "description": description,
            "confirmation_time": str(datetime.datetime.now().strftime("%Y-%m-%d")),
            "confirmation_hash": txn
        }

        confirmation_id = db.confirmations.insert_one(new_confirmation)
        return jsonify({'code': 200})
    except Exception as ex:
        return jsonify({"code": 400, "message":str(ex)})

@app.route("/retrieveConfirmation", methods=['GET'])
def retrieveConfirmation():

    try:
        project_id = request.args.get("project_id")
        result = list(db.confirmations.find({"project_id":ObjectId(project_id)}))
        # print(result)
        result_list = []
        num = 0
        for i in result:
            project = db.projects.find_one({"_id": i['project_id']})
            # Check the confirmation information from blockchain to make sure this confirmation is valid
            check = blockchainSetup.checkConfirmation(i['confirmation_hash'], project['project_solidity_id'],i['amount'])
            if(check):
                i['_id'] = str(i['_id'])
                i['project_id'] = str(i['project_id'])
                num += int(i['amount'])
                result_list.append(i)

        result1={'confirmations':result_list,'total_confirmation':num}
        return jsonify({"code": 200, "result": result1})
    except Exception as ex:
        return jsonify({"code": 400, "message": str(ex)})

def get_byte_image(image_path):
    img = Image.open(image_path, mode='r')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return encoded_img

@app.route("/retrieveProjectDetails",methods=['GET'])
def retrieveProjectDetails():

    try:
        result = db.projects.find_one({"_id":ObjectId(request.args.get("id"))})

        approval = blockchainSetup.checkProjectApproval(result['approval_hash'], result['project_solidity_id'])
        stop = blockchainSetup.checkProjectStop(result['approval_hash'], result['project_solidity_id'])

        if(not approval and not stop):
            return jsonify({"code": 400, "error": "This Project is still waiting for approval!"})
        if(stop):
            result['stop'] = "1"
        else:
            result['stop'] = "0"


        result['_id'] = str(result['_id'])
        image_path = './projectCover/'+ result['_id'] + '/cover.jpg'

        image = get_byte_image(image_path)
        result["image"] = image

        result['charity_id'] = str(result['charity_id'])
        charity = db.charities.find_one({"_id":ObjectId(result['charity_id'])})
        result['charity_name'] = charity['full_name']

        result['charity_description'] = charity['description']
        result['charity_number'] = charity['contact_number']
        result['charity_email'] = charity['email']
        result['charity_address'] = charity['physical_address']
        donations = list(db.donations.find({"project_id": ObjectId(result['_id'])}))

        num = 0
        for d in donations:
            donor = db.donors.find_one({"_id": d['donor_id']})
            check = blockchainSetup.checkDonation(d['donation_hash'], donor['eth_address'])
            if (check == True):
                num += int(d['amount'])
        # print(num)
        result['actual_amount'] = num
        result['fundTarget'] = int(result['fundTarget'])

        return jsonify({'code': 200, "result": result})
    except Exception as ex:
        return jsonify({"code": 400, "message":str(ex)})

@app.route("/registerProject", methods=['POST'])
def registerProject():
    projectId = request.form.get("projectId")

    try:
        if  projectId == "0":
            beneficiaryListFile = request.files["beneficiaryList"]
            df = pd.read_excel(beneficiaryListFile)
            if list(df.columns) != ["beneficiary", "remark"]:
                return jsonify({"code": 400, "message":"Invalid beneficiary file format."})

            beneficiaryList = []
            for index, row in df.iterrows():
                beneficiaryList.append({
                    "name": row["beneficiary"],
                    "remark": row["remark"]
                    })

            #register to blockchain
            charity = request.form.get("charityAddress")
            beneficiaryGainedRatio = request.form.get('beneficiaryGainedRatio')
            txn, numProjects = blockchainSetup.registerProject(charity, int(beneficiaryGainedRatio))
            # numProjects = 0
            # txn = blockchainSetup.registerProject(charity, int(beneficiaryGainedRatio))

            #store in DB
            new_project = {
                "projectName": request.form.get('projectName'),
                "projectCategory": request.form.get('projectCategory'),
                "project_solidity_id": numProjects, 
                "charity_id": ObjectId(request.form.get('charity_id')),
                "charityAddress": charity,
                "beneficiaryList": beneficiaryList, 
                "breakdownList": request.form.get('breakdownList'), 
                "expirationDate": request.form.get('expirationDate'), 
                "fundTarget": request.form.get('fundTarget'),
                "description": request.form.get("description"),
                "registration_hash": txn,
                "approval_hash": '',
            }
            project_id = str(db.projects.insert_one(new_project).inserted_id)

            #store cover image
            projectCover = request.files["projectCover"]
            folder_path = "./projectCover/" + project_id + "/"
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            filename = "cover.jpg"
            projectCover.save(os.path.join(folder_path, filename))

            #store beneficiary file
            folder_path = "./beneficiary/" + project_id + "/"
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            filename = "beneficiary.xlsx"
            #export df to excel
            df.to_excel(os.path.join(folder_path, filename), index=False)
    
            return jsonify({
                    "code": 200,
                    "project_id": project_id, 
                    })
        else:
            beneficiaryList = []
            beneficiaryListFile = request.files["beneficiaryList"]
            if "beneficiaryList" in request.files:
                df = pd.read_excel(beneficiaryListFile)
                if list(df.columns) != ["beneficiary", "remark"]:
                    return jsonify({"code": 400, "message":"Invalid beneficiary file format."})        
                for index, row in df.iterrows():
                    beneficiaryList.append({
                        "name": row["beneficiary"],
                        "remark": row["remark"]
                        })

                #store beneficiary file
                folder_path = "./beneficiary/" + projectId + "/"
                Path(folder_path).mkdir(parents=True, exist_ok=True)
                filename = "beneficiary.xlsx"
                #export df to excel
                df.to_excel(os.path.join(folder_path, filename), index=False)
            else: 
                print("file unchanged")
            update_dic = {
                        "projectName": request.form.get('projectName'),
                        "projectCategory": request.form.get('projectCategory'),
                        "breakdownList": request.form.get('breakdownList'), 
                        "expirationDate": request.form.get('expirationDate'), 
                        "fundTarget": request.form.get('fundTarget'),
                        "description": request.form.get("description"),
                        "approval_hash": '',
            }
            if len(beneficiaryList) > 0:
                update_dic["beneficiaryList"] = beneficiaryList

            #update in DB
            result = db.projects.find_one_and_update(
                    {"_id": ObjectId(projectId)},
                        {"$set":update_dic
                    })        

            if "projectCover" in request.files:
                projectCover = request.files["projectCover"]
                folder_path = "./projectCover/" + projectId + "/"
                Path(folder_path).mkdir(parents=True, exist_ok=True)
                filename = "cover.jpg"
                projectCover.save(os.path.join(folder_path, filename))
            else: 
                print("projectCover unchanged")
               
            return jsonify({
                    "code": 200,
                    "project_id": projectId, 
                    })

    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"code": 400,
            "message": str(ex)}
        )

@app.route("/getAllPendingProjects", methods=['GET'])
def getAllPendingProjects():
    try:
        db_result = db.projects
        result_list = []
        all_result = db_result.find(
            {"approval_hash": ''}
        )
        for result in all_result:
            result['_id'] = str(result['_id'])
            result['charity_id'] = str(result['charity_id'])
            result_list.append(result)

        return jsonify(
            {"code": 200,
            "items": result_list}
        )
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/getAllApprovedProjects", methods=['GET'])
def getAllApprovedProjects():
    try:
        db_result = db.projects
        result_list = []
        all_result = db_result.find(
            {"approval_hash": { "$ne": ''}}
        )
        # check whether project is approval  
        for result in all_result:
            result['_id'] = str(result['_id'])
            approval = blockchainSetup.checkProjectApproval(result["approval_hash"],result['project_solidity_id'])
            print(approval)
            if approval: 
                # check whether project met the target amount 
                donations = list(db.donations.find({"project_id": ObjectId(result['_id'])}))
                num = 0
                numDonors = 0 
                for d in donations:
                    donor = db.donors.find_one({"_id": d['donor_id']})
                    check = blockchainSetup.checkDonation(d['donation_hash'], donor['eth_address'])
                    if (check == True):
                        num += int(d['amount'])
                        numDonors = numDonors + 1
                if num < int(result['fundTarget']):
                    result['actual_amount'] = num
                    result['numDonors'] = numDonors
                    result['charity_id'] = str(result['charity_id'])
                    result_list.append(result)
            print(result)
        return jsonify(
            {"code": 200,
            "items": result_list}
        )
    except Exception as ex:
        return jsonify({
                "code":400,
                "message": str(ex)
            })

@app.route("/stopProject", methods=['POST'])
def stopProject():
    projects = db.projects 

    project_solidity_id = request.form.get('project_solidity_id')
    inspector = request.form.get('inspectorAddress')
    try:
        txn = blockchainSetup.stopProject(inspector, int(project_solidity_id))
        result = projects.find_one_and_update(
            {"project_solidity_id": int(project_solidity_id)},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        dic = {"txn": txn}
        return jsonify({
            "code": 200,
            "message": 'Project has been stopped'})
    except Exception as ex:
        return jsonify({
            "code": 400,
            "message":str(ex)})

@app.route("/beneficiaryFile", methods=['get'])
def getBeneficiaryListFile():
    projectId = request.args.get("id")
    file_path = "./beneficiary/" + projectId + "/beneficiary.xlsx"
    return send_file(file_path, attachment_filename='beneficiary.xlsx')

@app.route("/beneficiaryFileFormat", methods=['get'])
def getBeneficiaryFormatFile():
    file_path = "./beneficiary/beneficiary.xlsx"
    return send_file(file_path, attachment_filename='beneficiary.xlsx')

@app.route("/certificateFile", methods=['get'])
def getCertificateFile():
    charityAddress = request.args.get("address")
    file_path = "./certificate/" + charityAddress + "/certificate.pdf"
    return send_file(file_path, attachment_filename='certificate.pdf')

@app.route("/approveProject", methods=['POST'])
def approveProject():
    projects = db.projects 

    project_solidity_id = request.form.get('project_solidity_id')
    inspector = request.form.get('inspectorAddress')
    try:
        txn = blockchainSetup.approveProject(inspector, int(project_solidity_id))
        result = projects.find_one_and_update(
            {"project_solidity_id": int(project_solidity_id)},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        dic = {"txn": txn}
        return jsonify({
            "code": 200,
            "message": 'Project has been approved'})
    except Exception as ex:
        return jsonify({
            "code": 400,
            "message":str(ex)})

@app.route("/rejectProject", methods=['POST'])
def rejectProject():
    projects = db.projects

    project_solidity_id = request.form.get('project_solidity_id')
    inspector = request.form.get('inspectorAddress')

    try:
        txn = blockchainSetup.rejectProject(inspector, int(project_solidity_id))
        result = projects.find_one_and_update(
            {"project_solidity_id": int(project_solidity_id)},
            {"$set":{
                "approval_hash":txn
            }
            }
        )
        return jsonify({
            "code": 200,
            "message": "Project has been rejected"})
    except Exception as ex:
        return jsonify({
            "code": 400, 
            "message":str(ex)})

@app.route("/retrieveAllProjects", methods=['GET'])
def retrieveAllProjects():
    projects = db.projects
    try:
        result = list(projects.find({"approval_hash": { "$ne": ""}}))
        result_list = []
        for i in result:
            # Check the approval information from blockchain to make sure this project is valid
            check = blockchainSetup.checkProjectApproval(i['approval_hash'], i['project_solidity_id'])
            if(check):
                i['_id'] = str(i['_id'])
                i['charity_id'] = str(i['charity_id'])
                i['fundTarget'] = int(i['fundTarget'])
                image_path = './projectCover/'+ i['_id'] + '/cover.jpg'
                print(image_path)
                image = get_byte_image(image_path)
                i["image"] = image

                num = 0
                donations = list(db.donations.find({"project_id": ObjectId(i['_id'])}))
                for d in donations:
                    donor = db.donors.find_one({"_id": d['donor_id']})
                    check = blockchainSetup.checkDonation(d['donation_hash'], donor['eth_address'])
                    if (check == True):
                        num += int(d['amount'])
                i['actual_amount'] = num
                result_list.append(i)

        return jsonify({"code":200, "result": result_list})
    except Exception as ex:
        return jsonify({"code":400, "message":str(ex)})

@app.route("/retrieveDonorsByProject", methods=['GET'])
def retrieveDonorsByProject():
    try:
        project = db.projects.find_one({"_id":ObjectId(request.args.get("id"))})
        project['_id'] = str(project['_id'])

        donations = list(db.donations.find({"project_id": ObjectId(project['_id'])}))
        result_list = []
        for i in donations:
            donor = db.donors.find_one({"_id": i['donor_id']})
            # Check the donation information from blockchain to make sure this donation is valid
            check = blockchainSetup.checkDonation(i['donation_hash'],donor['eth_address'])
            if(check == True):
                i['_id'] = str(i['_id'])
                i['project_id'] = str(i['project_id'])
                i['donor_id'] = str(i['donor_id'])
                if(i['anonymous'] == 'true'):
                    i['donor'] = 'Anonymous Donor'
                else:
                    i['donor'] = donor['full_name'][0] + 'xxx' + donor['full_name'][-1]
                result_list.append(i)


            # print(donations)

        latestDonors = list(reversed(list(result_list)))

        return jsonify({"code":200, "latestDonors": latestDonors})
    except Exception as ex:
        return jsonify({"code":400,"latestDonors":[],"message":str(ex)})

@app.route("/donor/login", methods=['GET'])
def loginDonor():
    donors = db.donors
    try:
        results = donors.find_one({"username": request.args.get("username")})

        salt = results["password"][:32] # Get the salt you stored for *this* user
        key = results["password"][32:] # Get this users key calculated

        password_to_check = request.args.get("password") # The password provided by the user to check

        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'), # Convert the password to bytes
            salt, 
            100000
        )

        if ( len(results) and new_key == key):
            approval = blockchainSetup.checkDonorApproval(results["approval_hash"],results["eth_address"])
            reject = blockchainSetup.checkDonorReject(results["approval_hash"],results["eth_address"])
            if(approval):
                return jsonify(
                    {   
                        "code": 200,
                        "id": str(results["_id"]),
                        "username": results["username"],
                        "eth_address": results["eth_address"]
                     }
                )
            elif(reject):
                return jsonify({"code":400, "message": "Sorry, Your account is rejected!"})
            else:
                return jsonify({"code":400, "message": "Your account is still waiting for approval!"})

        else:
            return jsonify({"code":400, "message": "username or password not correct"})

    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {"error": "username or password not correct"}
        )

@app.route("/charity/login", methods=['GET'])
def loginCharity():
    charities = db.charities
    try:
        results = charities.find_one({"username": request.args.get("username")})

        salt = results["password"][:32] # Get the salt you stored for *this* user
        key = results["password"][32:] # Get this users key calculated

        password_to_check = request.args.get("password") # The password provided by the user to check

        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'), # Convert the password to bytes
            salt, 
            100000
        )

        if ( len(results) and key == new_key):
            approval = blockchainSetup.checkCharityApproval(results["approval_hash"],results["eth_address"])
            reject = blockchainSetup.checkCharityReject(results["approval_hash"],results["eth_address"])
            if approval:
                return jsonify(
                    {
                        "code":200,
                        "id": str(results["_id"]),
                        "username": results["username"],
                        "eth_address": results["eth_address"]
                    }
                )
            elif(reject):
                return jsonify({"code":400, "message": "Sorry, Your account is rejected!"})
            else:
                return jsonify({"code":400, "message": "Your account is still waiting for approval!"})
        else:
            return jsonify({
                "code": 400,
                "message": "username or password not correct"
                })
        
    except Exception as ex:
        print(ex)
        print(type(ex))
        return jsonify(
            {   
                "code": 400,
                "message": "username or password not correct"
            }
        )

@app.route("/admin/login", methods=['GET'])
def loginAdmin():
    if request.args.get("password") == "admin" and request.args.get("username") == "admin":
        return jsonify({
            "code": 200,
            "eth_address": blockchainSetup.inspectorAddress
            })
    else:
        return jsonify({"code": 400, "message": "Username and Password are not matched!"})

@app.route("/adddummydata",methods=['GET'])
def dummyData():

    i = 0;
    for i in range(3):
        # txn = blockchainSetup.registerOrganization(charity, request.form.get("full_name"))
        new_charity = {
            "username": "charity"+str(i),
            "password": "password"+str(i),
            "email":  "email"+str(i),
            "eth_address": "testing",
            "bank_account": "testing",
            "physical_address": "testing",
            "full_name": "charity name"+str(i),
            "contact_number": "123456",
            "financial_info": "213123",
            "description": "good charity balahbalahbalah",
            "registration_hash": "yeah",
            "approval_hash": "oh"
        }
        p = 0;
        charity_id = db.charities.insert_one(new_charity)
        for p in range(3):
            new_project = {
                "charity_id": charity_id.inserted_id,
                "project_name": "project_name"+str(i)+str(p),
                "beneficiaryListId": "beneficiary_list_id"+str(i)+str(p),
                "documentation": "documentation"+str(i)+str(p),
                "expiry_date": "2020-05-20",
                "target_amount": 10000,
                "description": "A good charity Project balah balah balah balah balah balah balah balah",
                "registration_hash": "yeah",
                "approval_hash": 'yes',
                "reject_hash": 'oh',
                'project_solidity_id':p
            }
            project_id = db.projects.insert_one(new_project)

    project = db.projects.find_one({"project_name": "project_name00"})

    q = 0;
    for q in range(10):
        new_donor = {
            "username": "donor"+str(q),
            "password": "password"+str(q),
            "email": "email"+str(q),
            "eth_address": "testing"+str(q),
            "bank_account": "testing"+str(q),
            "physical_address": "testing"+str(q),
            "full_name": "name"+str(q),
            "contact_number": "123456",
            "financial_info": "321321",
            "registration_hash": "success",
            "approval_hash": "success"
        }
        donor_id = db.donors.insert_one(new_donor)

        new_donation = {
            "amount": 10,
            "project_id": project["_id"],
            "donor_address": "testing"+str(q),
            "donation_hash": "success",
            "confirmed_hash": ''
        }
        donation_id = db.donations.insert_one(new_donation)

    return jsonify({"code":200})


if __name__ == "__main__":
    app.run(debug=True)


