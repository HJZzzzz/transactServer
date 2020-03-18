from web3 import Web3
import json


web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
accounts = web3.eth.accounts

with open("/blockchain/build/contracts/Project.json") as project:
    info_json = json.load(project)
abi = info_json["abi"]

projectContractAddress = '0x748E9E7fd703D4b3609c5DDdCc9CD856C87410f1'
projectContract = web3.eth.contract(abi=abi, address=projectContractAddress)


with open("/blockchain/build/contracts/Registration.json") as regist:
    info_json = json.load(regist)
abi = info_json["abi"]

registrationContractAddress = '0xe9E8785BCF7597c281da40Afdb4e0fc3a4260F2E'
registrationContract = web3.eth.contract(abi=abi, address=registrationContractAddress)


with open("/blockchain/build/contracts/Donation.json") as donation:
    info_json = json.load(donation)
abi = info_json["abi"]

donationContractAddress = '0x4EA0DB8c3EF54e8Cc8b22A759b7A705cE1c0CAC0'
donationContract = web3.eth.contract(abi=abi, address=donationContractAddress)

#let's do this