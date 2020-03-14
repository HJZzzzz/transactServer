pragma solidity ^0.5.0;

import "./Registration.sol";

contract Project {

  address owner = msg.sender;
  
  Registration registrationContract;

  constructor(Registration registrationAddress) public {
      registrationContract = registrationAddress;
  }


}