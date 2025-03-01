from web3 import Web3
from datetime import datetime, timezone
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_API_KEY = os.getenv("INFURA_API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
NETWORK = os.getenv("NETWORK", "sepolia")

infura_url = f"https://{"NETWORK"}.infura.io/v3/{INFURA_API_KEY}"
web3=Web3(Web3.HTTPProvider(infura_url))

#checking if contract is connected to blockchain
if web3.is_connected():
    print(" + connected to eth testnet")
else:
    print("X connection failed, check infura api key or something else ")

#this needs to get updated when I add more functions to smart contract
#recompile hardhat too
contract_abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "logId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "logHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "logType",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "LogAdded",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_logHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_logType",
          "type": "string"
        }
      ],
      "name": "addLog",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "logId",
          "type": "uint256"
        }
      ],
      "name": "getLog",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "logCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "logs",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "logHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "logType",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ] #put ABI from hardhat output here

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

#generate log hash
def hash_log(event_type, details):
    current_timestamp = datetime.now(timezone.utc).isoformat()


    log_data = {
        "event": event_type, 
        "details": details, 
        "timestamp": current_timestamp
    }

    log_string = json.dumps(log_data, sort_keys=True)
    return hashlib.sha256(log_string.encode()).hexdigest()

def log_security_event(event_type, details):
    account = web3.eth.account.privateKeyToAccount(PRIVATE_KEY)
    log_hash = hash_log(event_type, details)

    txn = contract.functions.addLog(log_hash, event_type).build_transaction({
        "from": account.address,
        "nonce": web3.eth.getTransactionCount(account.address),
        "gas": contract.functions.addLog(log_hash, event_type).estimate_gas({'from': account.address}),
        "gasPrice": web3.to_wei('10','gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key = PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f" + Log type: {event_type}")
    print(f" + Transaction Hash: {web3.to_hex(tx_hash)}")

#checking if log has been tampered by pulling log from blockchain, recomputing hash, and 
# comparing it to stored hashed log
def verify_log(log_id, original_event):
    try:
        log_data = contract.functions.getLog(log_id).call()
        stored_timestamp = log_data[0]
        stored_log_hash = log_data[1]
        stored_log_type = log_data[2]

        recomputed_hash = hash_log(stored_log_type, original_event)

        #compare hashes
        print("\n Log Verification:")
        print(f" Log ID: {log_id}")
        print(f" Timestamp: {stored_timestamp}")
        print(f" Log Type: {stored_log_type}")
        print(f" Stored Hash: {stored_log_hash}")
        print(f" Recomputed Hash: {recomputed_hash}")

        if stored_log_hash == recomputed_hash:
            print(" + LOG IS VALID, no tampering detected")
        else:
            print(" X WARNING: TAMPERING DETECTED!")
    except Exception as e:
        print(f"Error retrieving logs: {str(e)}")