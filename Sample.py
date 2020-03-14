from web3 import Web3
import json
import argparse
import requests
# from solc import compile_source
# from web3.utils.encoding import to_hex
with open("Dice.json") as f:
    info_json = json.load(f)
abi = info_json["abi"]


web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

diceContract = '0x639E02c3f8310501334d554aE7b7e8e47a9f02f3'

accounts = web3.eth.accounts
balance = web3.eth.getBalance(accounts[0],'latest')
print('balance@latest => {0}'.format(balance))
balance = web3.eth.getBalance(accounts[0],'earliest')
print('balance@earliest => {0}'.format(balance))

print(web3.eth.blockNumber)
print(web3.eth.getBlock('latest'))
# print(web3.eth.getBlock())

receipt = web3.eth.getTransactionReceipt(0x8ff7a3030b8e202efe26ff30242bdd790fa0f4b8c43c9b52679d717756781b3e)
print(receipt)


dice = web3.eth.contract(abi=abi, address=diceContract)

# txn = dice.call().getOwner()
# txn = dice.methods.getOwner()
# txn = dice.functions.getOwner(0)
txn = dice.functions.add(6,0).transact({'from':accounts[0],'value':web3.toWei(1,'ether')})
print(txn)
# print("Owner",dice.call().creator)



# only payable func can make txn in block--> limited eth per account(100)