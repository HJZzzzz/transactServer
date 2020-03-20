# transactServer

##To test blockchain module
###1. Open Command Prompt, initiate accounts with "ganache-cli -p 8545".
###2. Open another terminal, make sure you go into Blockchain folder (e.g. Desktop/transactServer/blockchain), check if your code affect the test cases using "truffle test". 

##To test flask app
###Note: if this is your first time, run this command "pip3 install -r requirements.txt".
###1. Open Command Prompt, initiate eth accounts with "ganache-cli -p 8545".
###2. Open another terminal, make sure you go into Blockchain folder (e.g. Desktop/transactServer/blockchain), deploy contracts using "truffle migration".
###3. Go to blockchainSetup.py to change your contract address from Step(2)
###4. Open a new terminal, and run "flask run"
###5. Use browser or postman to test