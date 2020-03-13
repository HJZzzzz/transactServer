pragma solidity ^0.5.0;

contract Registration {

  address owner = msg.sender;
  mapping(address => Donor) public donors;
  mapping(address => Inspector) public inspectors;


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


  uint256 numDonors = 0;
  uint256 numInspectors = 0;


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

}