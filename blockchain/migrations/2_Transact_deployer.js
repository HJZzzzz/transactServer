const Transact = artifacts.require("Transact");

module.exports = function(deployer) {
  deployer.deploy(Transact)
};
