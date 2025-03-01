//this file loads smart contract in frontend
import {ethers} from "ethers";
import contractABI from "./SecurityLogABI.json"; //deployed contract addess

const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;

export const getContract = async () => {
    if (!window.ethereum) throw new Error("MetaMask is not installed");

    const provider = new ethers.BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    return new ethers.Contract(CONTRACT_ADDRESS, contractABI.abi, signer);

};