const Registration = artifacts.require("Registration");
const Donation = artifacts.require("Donation");


module.exports = function(deployer) {
    deployer.then(() => {
        return deployer.deploy(Registration);
    }).then((regInstance => {
        console.log("Registration contract at address" + regInstance.address);
        return deployer.deploy(Donation, regInstance.address);
    })).then(donationInstance => {
        console.log("Donation contract at address" + donationInstance.address);
    })
  };
