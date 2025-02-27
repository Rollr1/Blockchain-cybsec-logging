// solidity smart contract

pragma solidity ^0.8.19;

contract securitylog {
    struct LogEntry {
        uint256 timestamp; //time that log was recorded
        string logHash; //hash of the log (SHA-256)
        string logType; //type of log (login attempt, etc.)
    }

//storing logs using a unique ID
    mapping(uint256 => LogEntry) public logs;
    uint256 public logCount = 0;

    event LogAdded(uint256 indexed logId, string logHash, string logType, uint256 timestamp);

//call this to add a hashed log to the blockchain
    function addLog(string memory _logHash, string memory _logType) public {
        logs[logCount] = LogEntry(block.timestamp, _logHash, _logType);
        emit LogAddded(logCount, _logHash, _logType, block.timestamp);
        logCount++;
    }

//retrieve a log entry by ID
    function getLog(uint256 logId) public view returns (uint256, string memory, string memory) {
        LogEntry memory logEntry = logs[logId];
        return (logEntry.timestamp, logEntry.logHash, logEntry.logType);
    }
}