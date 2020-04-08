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

    mapping(uint256 => donation) public donations;

    event madeDonation(address donor, address charityOrg, uint amount);
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
    function makeDonation(uint _amount, uint256 _projectId) public {
        // Check that the donor did not already exist:
        require(registrationContract.approvedDonor(msg.sender), 'Only approved donor can make registration.');
        address _charityAdd = projectContract.getOrganizationAddByProjectId(_projectId);
        require(registrationContract.approvedOrganization(_charityAdd));
        require( uint(projectContract.checkProjectStatus(_projectId)) == 1 , 'Can only make donation to approved project.');
        // Donation storage donation = donations[_donationId];
        // super._mint(msg.sender,_donationId);
        uint256 _donationId = numDonations++;
        donations[_donationId] = donation({
            id:_donationId,
            amount: _amount,
            from: msg.sender,
            to: _charityAdd,
            confirmed: false
        });
        emit madeDonation(msg.sender, _charityAdd, _amount);
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
        // emit DonationConfirmed(_donationId); --Jiayun: view cannot emit event
    }
}