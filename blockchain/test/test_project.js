const Registration = artifacts.require("Registration");
const Project = artifacts.require("Project");

contract("Project", accounts => {
    let registrationInstance;
    let projectInstance; 

    // user 1 is charity organization 
    const user1 = accounts[1];
    // user 2 is a registered inspector 
    const user2 = accounts[2];

    before(async () => {
        registrationInstance = await Registration.deployed();
        projectInstance = await Project.new(
            registrationInstance.address
        );
    });

    it('Register a new charity project', async() =>{
        let _owner = await registrationInstance.getOwner.call();
        await registrationInstance.registerOrganization(user1, 'NUS_SOC', {
            from: _owner
        });
        await registrationInstance.registerInspector(user2, 'Ruichun', {
            from: _owner 
        });
        let organizationId = await registrationInstance.getOrganizationIdByAddress.call(user1);
        let projectId = await projectInstance.registerProject.call(organizationId, 1, 1, 80);
        assert.equal(projectId.toNumber(), 0); 
    })

    it('Approve a project', async() =>{
        let organizationId = await registrationInstance.getOrganizationIdByAddress.call(user1);
        await projectInstance.registerProject(organizationId, 1, 1, 80);

        await projectInstance.approveProject(0, {
            from: user2
        });

        let state = await projectInstance.checkProjectStatus.call(0);
        assert.equal(state.toNumber(), 1)
    })

    it('Reject a project', async() =>{
        let organizationId = await registrationInstance.getOrganizationIdByAddress.call(user1);
        let projectId = await projectInstance.registerProject.call(organizationId, 1, 1, 80);

        await projectInstance.rejectProject(projectId, {
            from: user2
        });

        let state = await projectInstance.checkProjectStatus.call(projectId); 
        assert.equal(state.toNumber(), 2)
    })

});
  