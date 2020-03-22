pragma solidity ^0.5.0;

contract Registration {

  address owner = msg.sender;
  mapping(address => Donor) public donors;
  mapping(address => Inspector) public inspectors;
  mapping(address => Organization) public organizations;
  mapping(uint256 => Inspector) inspectorList;
  mapping(uint256 => address) public inspectorAddress; 


  struct Donor {
    uint256 id;
    string name;

    bool set;
  }

  struct Inspector {
    uint256 id;
    string name;

    bool set;
  }

  struct Organization {
    uint256 id;
    string name;

    bool set;
  }


  uint256 numDonors = 0;
  uint256 public numInspectors = 0;
  uint256 numOrganizations = 0;

event DonorApproval(address donor, address inspector);

  modifier onlyOwner() {
      require(msg.sender == owner);
      _;
  }

  modifier onlyInspector() {
      require(inspectors[msg.sender].set, 'Only Inspector can trigger this action.');
      _;
  }

  modifier onlyDonor() {
      require(donors[msg.sender].set, 'Only Donor can trigger this action.');
      _;
  }

  function registerInspector(address _inspectorAddress, string memory _inspectorName) public onlyOwner {
    uint256 _inspectorId = numInspectors++;
    Inspector storage inspector = inspectors[_inspectorAddress];
    inspectorList[_inspectorId] = inspector;
    inspectorAddress[_inspectorId] = _inspectorAddress; 
    
    // Check that the inspector did not already exist:
    require(!inspector.set, 'You cannot add existing inspector.');
    inspectors[_inspectorAddress] = Inspector({
        id: _inspectorId,
        name: _inspectorName,
        set: true
    });
  }


  function registerDonor(address _donorAddress, string memory _donorName) public{
    uint256 _donorId = numDonors++;
    Donor storage donor = donors[_donorAddress];
    // Check that the donor did not already exist:
    require(!donor.set, 'You cannot add existing donor.');
    donors[_donorAddress] = Donor({
        id: _donorId,
        name: _donorName,
        set: false
    });
  }

  function approveDonor(address _donorAddress) public onlyInspector{
    donors[_donorAddress].set = true;
    emit DonorApproval(_donorAddress,msg.sender);
  }

  function rejectDonor(address _donorAddress) public onlyInspector{
    donors[_donorAddress].set = false;
    //should we delete account?
  }

  // function suspendDonor(address _donorAddress) public onlyInspector{
  //   donors[_donorAddress].set = false;
  // }

  function updateDonor(address _donorAddress, string memory _donorName) public{
    // Check that the donor did not already exist:
    Donor storage donor = donors[_donorAddress];
    require(donor.set, 'You cannot update non-existing donor.');
    donors[_donorAddress].name = _donorName;
  }

  function deleteDonor(address _donorAddress) public {
    // Check that the donor did not already exist:
    Donor storage donor = donors[_donorAddress];
    require(donor.set, 'You cannot delete non-existing donor.');
    delete donors[_donorAddress];
  }

  function approvedDonor(address _donorAddress) public view returns (bool){
    return donors[_donorAddress].set;
    
  }

  function getDonorName(address _donorAddress) public view returns (string memory){
    return donors[_donorAddress].name;
    
  }

  function getInspectorName(address _inspectorAddress) public view returns (string memory){
    return inspectors[_inspectorAddress].name;
    
  }

  function registerOrganization(address _organizationAddress, string memory _organizationName) public{
    uint256 _organizationId = numOrganizations++;
    Organization storage organization = organizations[_organizationAddress];
    // Check that the charity organization did not already exist:
    require(!organization.set, 'You cannot add existing organization.');
    organizations[_organizationAddress] = Organization({
        id: _organizationId,
        name: _organizationName,
        set: false
    });
  }

  function approveOrganization(address _organizationAddress) public onlyInspector{
    organizations[_organizationAddress].set = true;
  }

  function rejectOrganization(address _organizationAddress) public onlyInspector{
    organizations[_organizationAddress].set = false;
  }

  function updateOrganization(address _organizationAddress, string memory _organizationName) public{
    Organization storage organization = organizations[_organizationAddress];
    require(organization.set, 'You cannot update non-existing organization.');
    organizations[_organizationAddress].name = _organizationName;
  }

  function deleteOrganization(address _organizationAddress) public {
    // Check that the donor did not already exist:
    Organization storage organization = organizations[_organizationAddress];
    require(organization.set, 'You cannot delete non-existing organization.');
    delete organizations[_organizationAddress];
  }

  function approvedOrganization(address _organizationAddress) public view returns (bool){
    return organizations[_organizationAddress].set;
    
  }

  function getOrganizationName(address _organizationAddress) public view returns (string memory){
    return organizations[_organizationAddress].name;
    
  }
  
  function getNumOfInspectors() public view returns(uint256){
    return numInspectors;
  }
  
  function getInspectorAddressById(uint256 inspectorId) public view returns(address){
    return inspectorAddress[inspectorId];
  }

  function getOrganizationIdByAddress(address organizationAddress) public view returns(uint256){
    return organizations[organizationAddress].id; 
  }

  function getOwner() public view returns(address){
    return owner;
  }

  function getInspectorAddress(uint256 inspectorId) public view returns(address){
    return inspectorAddress[inspectorId]; 
  }

}