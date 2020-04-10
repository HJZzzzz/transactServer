from web3 import Web3
import json
from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    HexStr,
)
import hashlib

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
accounts = web3.eth.accounts

inspectorAddress = web3.eth.accounts[0]

with open("./blockchain/build/contracts/Project.json") as project:
    info_json = json.load(project)
abi = info_json["abi"]

projectContractAddress = '0xA4f6Da7d83E427aAa52b432C8D1ddE5eB823Fa27'
projectContract = web3.eth.contract(abi=abi, address=projectContractAddress)

with open("./blockchain/build/contracts/Registration.json") as regist:
    info_json = json.load(regist)
abi = info_json["abi"]

registrationContractAddress = '0x88e884fA870F014a5C466baf221e1204A6d65D1a'
registrationContract = web3.eth.contract(abi=abi, address=registrationContractAddress)


with open("./blockchain/build/contracts/Donation.json") as donation:
    info_json = json.load(donation)
abi = info_json["abi"]

donationContractAddress = '0x4aFE2CF6a4D44cCf016b2d9b7ffC8BCaF6A6596b'
donationContract = web3.eth.contract(abi=abi, address=donationContractAddress)

def make_donation(amount, pid, donor):
    # To protect user privacy, we will use sha256 to hash the donor' eth address
    hash = encrypt_string(donor)
    txn = donationContract.functions.makeDonation(amount, pid,hash).transact({'from': donor})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def confirmMoney(amount, pid, charity):
    txn = donationContract.functions.confirmMoney(amount, pid).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()


def registerInspector(address):
    print(address)
    # print(type(address))
    # print(accounts[0])
    # print(type(accounts[0]))
    txn = registrationContract.functions.registerInspector(address, "inspector").transact({'from': accounts[0]})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    # print("111")
    # print(txn)
    # print(type(txn))
    # print("222")
    # print(receipt)
    print(receipt.transactionHash)
    print(type(receipt.transactionHash))
    # print(receipt['from'])
    # print(receipt['to'])

    return receipt.transactionHash.hex()


def registerDonor(address, name):
    txn = registrationContract.functions.registerDonor(address,name).transact({'from':address})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()


def approveDonor(donor,inspector):
    hash = encrypt_string(donor)
    txn = registrationContract.functions.approveDonor(donor, hash).transact({'from':inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def rejectDonor(donor, inspector): 
    txn = registrationContract.functions.rejectDonor(donor).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()
    
def updateDonor(donor, name):
    txn = registrationContract.functions.updateDonor(donor, name).transact({'from': donor})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex() 


def getDonorDetails(donor):
    txn = registrationContract.functions.getOrganizationName(donor).call({'from': donor})
    return txn


def registerOrganization(charity, name):
    txn = registrationContract.functions.registerOrganization(charity, name).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()


def approveOrganization(charity, inspector):
    txn = registrationContract.functions.approveOrganization(charity).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn) 
    print(receipt.transactionHash.hex())
    return receipt.transactionHash.hex()


def rejectOrganization(charity, inspector):
    txn = registrationContract.functions.rejectOrganization(charity).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def updateOrganization(charity, name):
    txn = registrationContract.functions.updateOrganization(charity, name).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def deleteOrganization(charity):
    txn = registrationContract.functions.deleteOrganization(charity).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def approvedOrganization(charity):
    txn = registrationContract.functions.approvedOrganization(charity).call({'from': charity})
    return txn


def getOrganizationName(charity):
    txn = registrationContract.functions.getOrganizationName(charity).call({'from': charity})
    return txn


def confirmReceiveMoney(donation, charity):
    txn = donationContract.functions.confirmReceiveMoney(donation).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def registerProject(charity, beneficiaryGainedRatio):
    numProjects = registrationContract.functions.numProjects().call()
    txn = registrationContract.functions.registerProject(beneficiaryGainedRatio).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex(), numProjects


def approveProject(inspector, projectId):
    int_id = int(projectId)
    txn = registrationContract.functions.approveProject(int_id).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def rejectProject(inspector, projectId):
    int_id = int(projectId)
    txn = registrationContract.functions.rejectProject(int_id).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()

def stopProject(inspector, projectId):
    int_id = int(projectId)
    txn = registrationContract.functions.stopProject(int_id).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    return receipt.transactionHash.hex()


def checkDonorApproval(txn_hash,donor):
    try:
        receipt = web3.eth.getTransactionReceipt(txn_hash)
        logs = registrationContract.events.DonorApproval().processReceipt(receipt)
        # print(logs)
        if(logs[0]['args']['donor']==encrypt_string(donor)):
            # print(logs[0]['args']['donor'])
            return True
        return False
    except Exception as ex:
        print(ex)
        return False
        
def checkCharityApproval(txn_hash, charity):
    try:
        receipt = web3.eth.getTransactionReceipt(txn_hash)
        logs = registrationContract.events.OrganizationApproval().processReceipt(receipt)

        if(logs[0]['args']['organization']==charity):
            return True
        return False
    except Exception as ex:
        print(ex)
        return False

def checkProjectApproval(txn_hash,project_solidity_id):
    try:
        receipt = web3.eth.getTransactionReceipt(txn_hash)

        logs = registrationContract.events.ApprovalProject().processReceipt(receipt)
        print(logs)
        if(logs [0]['args']['projectId']== project_solidity_id):
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False

def checkDonation(txn_hash,donor_address):

    try:
        receipt = web3.eth.getTransactionReceipt(txn_hash)

        logs = donationContract.events.MadeDonation().processReceipt(receipt)
        # To protect user privacy, we will use sha256 to hash the donor' eth address
        # Here we will hash the donor's eth address to check whether the hashed values are same
        if(logs [0]['args']['donor']== encrypt_string(donor_address)):
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False

def checkConfirmation(txn_hash,project_solidity_id,amount):
    try:
        receipt = web3.eth.getTransactionReceipt(txn_hash)
        logs = donationContract.events.MadeConfirmation().processReceipt(receipt)
        if(logs [0]['args']['projectId']== project_solidity_id and logs [0]['args']['amount']== int(amount)):
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False



def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature