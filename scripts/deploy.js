const hre = require("hardhat");

async function main() {
    const SecurityLog = await hre.ethers.getContractFactory("SecurityLog");
    const securityLog = await SecurityLog.deploy();
    await securityLog.deployed();

    console.log("SecurityLog deployed to:", securityLog.address);

}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});