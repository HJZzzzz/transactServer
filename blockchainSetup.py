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

# Registration contract 
inspector_hash = registrationContract.functions.registerInspector(accounts[0], 'ruichun')
charityOrganization_hash = registrationContract.functions.registerOrganization(accounts[1], 'nus_soc')

# Project contract 
# Charity organization register a project 
organizationId = registrationContract.methods.getOrganizationIdByAddress(accounts[1]).call()
# for now, use dummy beneficiaryListId, dummy documentationId and dummy beneficiaryGainedRatio
project_hash_1 = projectContract.functions.registerProject(organizationId, 1, 1, 80).call({from: accounts[1]})
project_hash_2 = projectContract.functions.registerProject(organizationId, 1, 1, 80).call({from: accounts[1]})
# Inspector approve a project 
approve_project_hash = projectContract.functions.approveProject(0).call({from: accounts[0]})

# Inspector reject a project 
reject_project_hash = projectContract.functions.rejectProject(1).call({from: accounts[0]})

