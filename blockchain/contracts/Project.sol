pragma solidity ^0.5.0;

import "./Registration.sol";

contract Project {
    Registration registrationContract;

    constructor(Registration registrationAddress) public {
        registrationContract = registrationAddress;
    }
    address _owner = msg.sender;

    enum projectState { pending, approved, rejected }
    struct CharityProject {
        address projectOrganizationAdd;
        uint256 beneficiaryGainedRatio;
        
        projectState state; 
        uint256 numOfDonationReceived; 
        uint256 amountOfDonationReceived; 
        uint256 amountOfDonationBeneficiaryReceived; 
    }

    mapping(uint256 => CharityProject) public projectList; 
    
    uint256 public numProjects = 0; 
    
    event ApprovalProject(address inspector, uint256 projectId);
    event RejectProject(address inspector, uint256 projectId);
    event RegisterProject(address organizationAdd, uint256 projectId);
    event DistributeDonation(uint256 donationAmount, uint256 projectId);

    function registerProject(uint256 beneficiaryGainedRatio) public returns (uint256){
        require(registrationContract.approvedOrganization(msg.sender), 'Only approved organisation can create project.');
        CharityProject memory newProject = CharityProject(
            msg.sender, 
            beneficiaryGainedRatio,
            projectState.pending, 
            0,
            0,
            0
        );
        uint256 newProjectId = numProjects++; 
        projectList[newProjectId] = newProject; 
        
        emit RegisterProject(msg.sender, newProjectId);
        return newProjectId; 
    }
    
    function approveProject(uint256 projectId) public onlyOwner() {
        require(
            projectList[projectId].state == projectState.pending,
            "Cannot deal with accepted or rejected projects"
        );
        projectList[projectId].state = projectState.approved;
        emit ApprovalProject(msg.sender, projectId);
    }
    
    function rejectProject(uint256 projectId) public onlyOwner() {
        require(
            projectList[projectId].state == projectState.pending,
            "Cannot deal with accepted or rejected projects"
        );
        projectList[projectId].state = projectState.rejected;
        emit RejectProject(msg.sender, projectId);
    }
    
    function checkProjectStatus(uint256 projectId) public view returns (projectState){
        return projectList[projectId].state;
    }

    // function getInspectorIdByProjectId(uint256 projectId) public view returns(uint256){
    //     return projectList[projectId].inspectorId;
    // }
    
    // function stopProject
    function getOrganizationAddByProjectId(uint256 projectId) public view returns(address){
        return projectList[projectId].projectOrganizationAdd;
    }

    function distributeDonation(uint256 donationAmount, uint256 projectId) public{
        projectList[projectId].numOfDonationReceived = projectList[projectId].numOfDonationReceived + 1;
        projectList[projectId].amountOfDonationReceived += donationAmount;
        projectList[projectId].amountOfDonationBeneficiaryReceived += donationAmount * projectList[projectId].beneficiaryGainedRatio / 100;

        emit DistributeDonation(donationAmount, projectId);
    }
    
    modifier onlyOwner() {
        require(msg.sender == _owner, "Invalid owner");
        _;
    }
}