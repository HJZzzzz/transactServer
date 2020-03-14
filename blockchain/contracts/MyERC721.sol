pragma solidity ^0.5.0;
import "../node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract MyERC721 is ERC721{
    
    
    struct donation{
        uint256 id;
        uint256 amount;
        address donor;
        address charity;
        address owner;
        address prevOwner;
    }
    
    
    address _owner = msg.sender;
    
    mapping(uint256 => donation) public donations;
    
    constructor() public {
        _owner = msg.sender;
    }
    
    function createDonation(uint256 id, uint256 amount, address donor, address charity) public {
        require(msg.sender == _owner,"You r not the owner of this contract");
        
        super._mint(msg.sender,id);
        
        donation memory newDonation = donation(
            id,
            amount,
            donor,
            charity,
            donor,
            address(0)
            );
            
        donations[id] = newDonation;
        
    }
    
    
    function transfer(uint256 id, address newOwner) public ownerOnly(id){
        
        super.transferFrom(msg.sender,newOwner,id);
        
        donations[id].prevOwner = donations[id].owner;
        donations[id].owner = newOwner;
        
    }
    
    function getOwner(uint256 Id) external view validDonationId(Id) returns (address) {
        return donations[Id].owner;
    }
    
    function getPrevOwner(uint256 Id) external view validDonationId(Id) returns(address) {
        
        return donations[Id].prevOwner;
    }
    
    modifier ownerOnly(uint256 id) {
        require(donations[id].owner == msg.sender,"You r not the owner of this card");
        _;
    }
    
    modifier validDonationId(uint256 Id) {
        require(super._exists(Id), "This card does not exists");
        _;
    }
    
}