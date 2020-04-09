pragma solidity ^0.5.0;
//import "../node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
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

    mapping(uint256 => donation) public donations;

    event MadeDonation(address donor, address charityOrg, uint amount);
    event DonationConfirmed(uint donationId);

    struct donation {
        uint id;
        uint amount;
        address from;
        address to;

        bool confirmed;
    }

    uint256 numDonations = 0;

    //to transfer to projectIdOwner
    function makeDonation(uint _amount, uint256 _projectId) public returns (uint256) {
        require(registrationContract.approvedDonor(msg.sender), 'Only approved donor can make donation');
        require(registrationContract.approvedOrganization(projectContract.getOrganizationAddByProjectId(_projectId)), 'Only approved organization can accept donation');
        require(uint(projectContract.checkProjectStatus(_projectId)) == 1, 'Only approved project can accept donation');
        
        uint256 _donationId = numDonations++;
        address _charity = projectContract.getOrganizationAddByProjectId(_projectId);
        
        donation memory newDonation = donation(
            _donationId,
            _amount,
            msg.sender,
            msg.sender,
            false
        );
        donations[_donationId] = newDonation;
        emit MadeDonation(msg.sender, msg.sender, _amount);
        return _donationId;
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
        // emit DonationConfirmed(_donationId); --Jiayun: view cannot emit event
    }
}