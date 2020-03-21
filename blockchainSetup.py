from web3 import Web3
import json
from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    HexStr,
)


web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
accounts = web3.eth.accounts

with open("./blockchain/build/contracts/Project.json") as project:
    info_json = json.load(project)
abi = info_json["abi"]

projectContractAddress = '0x702F71AA1e3f406555C8d78f20Df7B66890eF3cc'
projectContract = web3.eth.contract(abi=abi, address=projectContractAddress)


with open("./blockchain/build/contracts/Registration.json") as regist:
    info_json = json.load(regist)
abi = info_json["abi"]

registrationContractAddress = '0x22D29CA0b4a96C75034815B49Da07905cC4A28d1'
registrationContract = web3.eth.contract(abi=abi, address=registrationContractAddress)


with open("./blockchain/build/contracts/Donation.json") as donation:
    info_json = json.load(donation)
abi = info_json["abi"]

donationContractAddress = '0x1571F443450d604EEcD451F627c4E23720060A20'
donationContract = web3.eth.contract(abi=abi, address=donationContractAddress)


def make_donation(charity, amount, pid, donor):
    txn = donationContract.functions.makeDonation(charity, amount, pid)
    txn = txn.transact({'from': donor})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()



def registerInspector(address):
    # 0x95231d6698314d6962ff55f9e518a7e4880b10a66f91c4cb38c88ac769ade1a9
    # print(address)
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
    txn = registrationContract.functions.registerDonor(address, name).transact({'from':address})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()


def approveDonor(donor,inspector):
    txn = registrationContract.functions.approveDonor(donor).transact({'from':inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def rejectDonor(donor,inspector):
    txn = registrationContract.functions.rejectDonor(donor).transact({'from':inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def updateDonor(donor,name):
    txn = registrationContract.functions.updateDonor(donor,name).transact({'from':donor})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()    

def deleteDonor(donor):
    txn = registrationContract.functions.deleteDonor(donor).transact({'from': donor})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def registerOrganization(charity):
    txn = registrationContract.functions.registerOrganization(charity, "charity organization acct1").transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def approveOrganization(charity, inspector):
    txn = registrationContract.functions.approveOrganization(charity).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def rejectOrganization(charity, inspector):
    txn = registrationContract.functions.rejectOrganization(charity).transact({'from': inspector})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex() 

def updateOrganization(charity):
    txn = registrationContract.functions.updateOrganization(charity, "charity organization acct2").transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def deleteOrganization(charity):
    txn = registrationContract.functions.deleteOrganization(charity).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def approvedOrganization(charity):
    txn = registrationContract.functions.approvedOrganization(charity).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def getOrganizationName(charity):
    txn = registrationContract.functions.getOrganizationName(charity).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()

def confirmReceiveMoney(donation, charity):
    txn = donationContract.functions.confirmReceiveMoney(donation).transact({'from': charity})
    receipt = web3.eth.waitForTransactionReceipt(txn)
    print(receipt)
    return receipt.transactionHash.hex()