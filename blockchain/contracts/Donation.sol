pragma solidity ^0.5.0;
import "../node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./Registration.sol";
import "./Project.sol";

contract Donation is ERC721 {

    address owner = msg.sender;
  
    Registration registrationContract;
    Project projectContract;

    constructor(Registration registrationAddress, Project projectAddress) public {
        registrationContract = registrationAddress;
        projectContract = projectAddress;
    }

    mapping(uint256 => Donation) public donations;

    event madeDonation(address donor, address charityOrg, uint amount);

    struct Donation {
        uint id;
        uint amount;
        address from;
        address to;

        bool confirmed;
    }

    uint256 numDonations = 0;

    //to transfer to projectIdOwner
    function makeDonation(address _charityOrgAddress, uint _amount, uint256 _projectId) public {
        uint256 _donationId = numDonations++;
        // Check that the donor did not already exist:
        require(registrationContract.approvedDonor(msg.sender), 'Only approved donor can make registration.');
        // Donation storage donation = donations[_donationId];
        // super._mint(msg.sender,_donationId);
        donations[_donationId] = Donation({
            id:_donationId,
            amount: _amount,
            from: msg.sender,
            to: _charityOrgAddress,
            confirmed: false
        });
        emit madeDonation(msg.sender, _charityOrgAddress, _amount);
        projectContract.distributeDonation( _amount, _projectId);
    }

    function confirmReceiveMoney(uint256 _donationId) public {
        require(donations[_donationId].to == msg.sender, 'Only the receiptor of the donation can confirm.' );
        donations[_donationId].confirmed = true;
        // burn token
    }

    // function distributeDonation(uint256 donationAmount, uint256 projectId) public{
    //     projectContract.projectList[projectId].numOfDonationReceived = projectContract.projectList[projectId].numOfDonationReceived + 1;
    //     projectContract.projectList[projectId].amountOfDonationReceived += donationAmount;
    //     projectContract.projectList[projectId].amountOfDonationBeneficiaryReceived += donationAmount * projectContract.projectList[projectId].beneficiaryGainedRatio;
    // }
    
    function confirmedDonation(uint256 _donationId) public view returns (bool){
        return donations[_donationId].confirmed;
    
    }
}