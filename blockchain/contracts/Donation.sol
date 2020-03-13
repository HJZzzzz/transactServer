pragma solidity ^0.5.0;

import "./Registration.sol";

contract Donation {

  address owner = msg.sender;
  
  Registration registrationContract;

  constructor(Registration registrationAddress) public {
      registrationContract = registrationAddress;
  }

  mapping(uint256 => Donation) public donations;

  

}