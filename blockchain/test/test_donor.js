const Registration = artifacts.require("Registration");
const Project = artifacts.require("Project");
const Donation = artifacts.require("Donation");
const MyERC721 = artifacts.require("MyERC721");

contract(Registration, accounts => {

    let networkOwner = accounts[0];
    let donor1 = accounts[1];
    let donor2 = accounts[2];
    let inspector1 = accounts[3];
    let charityOrg1 = accounts[4];

    let registration;
    let donation;
    before(async () => {
    registration = await Registration.deployed({from:networkOwner});
    project= await Project.new(registration.address, {from:networkOwner});
    donation = await Donation.new(registration.address, project.address, {from:networkOwner});
    erc = await MyERC721.deployed({from:networkOwner});
    });

    it("Should deploy contract and create inspector 1", async() => {
        await registration.registerInspector(inspector1,"Terry",{from:networkOwner});
        let result = await registration.getInspectorName(inspector1);
        // console.log('result', result);
        assert.strictEqual(
            result,
            "Terry",
            'createInspector() did not create Inspector 1'
          );
      
     });

     it("Should create donor1", async() => {
        await registration.registerDonor(donor1,"Jake",{from:donor1});
        let result1 = await registration.getDonorName(donor1);
        let result2 = await registration.approvedDonor(donor1);
        // console.log('result', result);
        assert.strictEqual(
            result1,
            "Jake",
            'createDonor() did not create Donor 1'
          );

          assert.strictEqual(
            result2,
            false,
            'createDonor() did not create Donor 1'
          ); 
      
     });

     it("Shouldn't approve donor1", async() => {
        try{ 
        await registration.approveDonor(donor1);
        await registration.approvedDonor(donor1);
        }catch{
            'Only Inspector can trigger this action.'
        }
     });

     it("Should approve donor1 by inspector", async() => {
        await registration.approveDonor(donor1,{from:inspector1});
        let result = await registration.approvedDonor(donor1);
        // console.log('result', result);
        assert.strictEqual(
            result,
            true,
            'approveDonor() did not approve Donor 1'
          );
      
     });

     it("Should reject donor1 by inspector", async() => {
        await registration.rejectDonor(donor1,{from:inspector1});
        let result = await registration.approvedDonor(donor1);
        // console.log('result', result);
        assert.strictEqual(
            result,
            false,
            'rejectDonor() did not reject Donor 1'
          );
      
     });

     it("Should update donor1's name", async() => {
        await registration.approveDonor(donor1,{from:inspector1});
        await registration.updateDonor(donor1,"Jake Peralta",{from:donor1});
        let result = await registration.getDonorName(donor1);
        // console.log('result', result);
        assert.strictEqual(
            result,
            "Jake Peralta",
            'updateDonor() did not update Donor 1'
          );
      
     });

     it("Should delete donor1", async() => {
        await registration.deleteDonor(donor1,{from:donor1});
        let result = await registration.approvedDonor(donor1);
        // console.log('result', result);
        assert.strictEqual(
            result,
            false,
            'deleteDonor() did not delete Donor 1'
          );
      
     });

     it("Shouldn't update donor2's name", async() => {
        try{ 
            await registration.updateDonor(donor2,"Holt",{from:donor2});
        }catch(error){
            assert(error, "You cannot update non-existing donor.");
        }
      
     });

     it("Shouldn't delete donor2's name", async() => {
        try{ 
            await registration.deleteDonor(donor2,"Holt",{from:donor2});
        }catch(error){
            assert(error, "You cannot delete non-existing donor.");
        }
      
     });

     it("Should make registration", async() => {
        await registration.registerDonor(donor2,"Holt",{from:donor2}); 
        await registration.approveDonor(donor2,{from:inspector1});
        let result = await donation.makeDonation(charityOrg1, 100, {from:donor2});
        // console.log("result", result.logs[0].event);
        // Check event
        assert.equal(result.logs[1].event,
        'madeDonation',
        'The madeDonation event is emitted');
      
     });

     it("Should confirm receipt of money", async() => {
        await donation.confirmReceiveMoney(0, {from: charityOrg1});
        let result = await donation.confirmedDonation(0);
        // console.log("result", result.logs[0].event);
        // Check event
        assert.equal(result,
        true,
        'The confirmReceiveMoney() does not confirm receipt of Money.');
      
     });



});