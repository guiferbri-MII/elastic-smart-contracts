/*
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Gateway, Wallets } = require('fabric-network');
const path = require('path');
const fs = require('fs');
const { exit } = require('process');

const dir = '../'
var paths = [];
var chaincodes = [];
var dataStorageContracts = [];
var calculationStorageContracts = [];
var numberStoragesList = [];


let pro = new Promise((res,rej) => {
    fs.readdir(dir,(err,files) => {
   
        paths= paths.concat(files.filter((path)=> {
           return path != 'esc';
        }))
        res(true)   
    })
})
    
    
pro.then(()=>{
    for(let i = 0; i<paths.length; i++){

        let a = require('../'+paths[i]+'/myESC')

        chaincodes.push(a.config.chaincodeName);
        dataStorageContracts.push(a.config.dataStorageContract);
        calculationStorageContracts.push(a.config.calculationStorageContract);

    }
    main(chaincodes,dataStorageContracts,calculationStorageContracts);
})


async function main(chaincodes,dataStorageContracts,calculationStorageContracts) {
    try {
        // load the network configuration
        const ccpPath = path.resolve(__dirname, '..',  '..', 'governify-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        const ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

        // Create a new file system based wallet for managing identities.
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);

        // Check to see if we've already enrolled the user.
        const identity = await wallet.get('admin');
        if (!identity) {
            console.log('An identity for the user "admin" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            return;
        }


        // Create a new gateway for connecting to our peer node.
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'admin', discovery: { enabled: true, asLocalhost: true } });

        // Get the network (channel) our contract is deployed to.
        const network = await gateway.getNetwork('governifychannel');

        // Get the contract from the network.
        

        for(let i =0; i<chaincodes.length; i++){
            let contract = network.getContract(chaincodes[i]);

      
            await contract.submitTransaction(dataStorageContracts[i]);
        
            
                
            await contract.submitTransaction(calculationStorageContracts[i]);
            console.log()

        }
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        process.exit(1);
    }
}








