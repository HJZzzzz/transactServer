pragma solidity ^0.5.0;

import "./Registration.sol";
import "./Project.sol";

contract Donation {

  address owner = msg.sender;
  
  Registration registrationContract;
  Project projectContract;

  constructor(Registration registrationAddress, Project projectAddress) public {
      registrationContract = registrationAddress;
      projectContract = projectAddress;
  }

  mapping(uint256 => Donations) public donations;

  event madeDonation(address donor, address charityOrg, uint amount);

  struct Donations {
  uint amount;
  address from;
  address to;

  bool confirmed;
  }

  uint256 numDonations = 0;

  //to transfer to projectIdOwner
  function makeDonation(address _charityOrgAddress, uint _amount) public {
    uint256 _donationId = numDonations++;
    // Check that the donor did not already exist:
    require(registrationContract.approvedDonor(msg.sender), 'Only approved donor can make registrationion.');
    // Donation storage donation = donations[_donationId];
    donations[_donationId] = Donations({
        amount: _amount,
        from: msg.sender,
        to: _charityOrgAddress,
        confirmed: false
    });
    emit madeDonation(msg.sender, _charityOrgAddress, _amount);
    //distributeDonation(uint256 uint256 _amount, uint256 _projectId)
  }

  function confirmReceiveMoney(uint256 _donationId) public {
    require(donations[_donationId].to == msg.sender, 'Only the receiptor of the donation can confirm.' );
    donations[_donationId].confirmed = true;
  }

  function confirmedDonation(uint256 _donationId) public view returns (bool){
    return donations[_donationId].confirmed;
    
  }

}