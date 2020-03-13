pragma solidity ^0.5.0;

import "./Registration.sol";

contract Donation {

  address owner = msg.sender;
  
  Registration registrationContract;

  constructor(Registration registrationAddress) public {
      registrationContract = registrationAddress;
  }

  mapping(uint256 => Donation) public donations;

  event madeDonation(address donor, address charityOrg, uint amount);

  struct Donation {
  uint amount;
  address from;
  address to;
  }

  uint256 numDonations = 0;

  //to transfer to projectIdOwner
  function makeDonation(address _charityOrgAddress, uint _amount) public {
    uint256 _donationId = numDonations++;
    // Check that the donor did not already exist:
    require(registrationContract.approvedDonor(msg.sender), 'Only approved donor can make registrationion.');
    // Donation storage donation = donations[_donationId];
    donations[_donationId] = Donation({
        amount: _amount,
        from: msg.sender,
        to: _charityOrgAddress
    });
    emit madeDonation(msg.sender, _charityOrgAddress, _amount);
    //distributeDonation(uint256 uint256 _amount, uint256 _projectId)
  }



}