const Registration = artifacts.require("Registration");
const Project = artifacts.require("Project");
const Donation = artifacts.require("Donation");
//const ERC721 = artifacts.require("ERC721");


let registration;

module.exports = function(deployer) {
    deployer.then(() => {
        return deployer.deploy(Registration);
    }).then((regInstance => {
        console.log("Registration contract at address" + regInstance.address);
        registration = regInstance.address;
        return deployer.deploy(Project, regInstance.address);
    })).then((projectInstance => {
        console.log("Project contract at address" + projectInstance.address);
        project = projectInstance.address;
        return deployer.deploy(Donation, registration, projectInstance.address);
    })).then(donationInstance => {

        console.log("Donation contract at address" + donationInstance.address);
        // return deployer.deploy(Donation, project, registration);
    })
    // .then(donationInstance => {
    //     console.log("Donation contract at address" + donationInstance.address);
    //     //return deployer.deploy(ERC721);
    // })
    // .then(erc=>{
    //     console.log("ERC721 contract at address" + erc.address);
    // })
  };