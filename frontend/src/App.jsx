import { useState, useEffect } from "react";
import { getContract } from "./contract";

function App() {
  const [logs, setLogs] = useState([]);
  const [eventType, setEventType] = useState("");
  const [details, setDetails] = useState("");
  const [account, setAccount] = useState(null);

  useEffect(() => {
    connectWallet().then(() => {
      fetchLogs(); // ✅ Fetch logs only after wallet is connected
    });
  }, []);

  useEffect(() => {
    getContract()
      .then(contract => {
        console.log("✅ Contract loaded successfully:", contract);
      })
      .catch(error => {
        console.error("❌ Contract load failed:", error); // ✅ Fixed typo
      });
  }, []);

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
        setAccount(accounts[0]);
      } catch (error) {
        if (error.code === 4001) {
          alert("Connection request denied. Please approve MetaMask.");
        } else {
          console.error("Error connecting to MetaMask:", error);
        }
      }
    } else {
      alert("MetaMask isn't installed. Please install it.");
    }
  };

  const fetchLogs = async () => {
    try {
        const contract = await getContract();  // ✅ Ensure contract is properly awaited
        if (!contract) throw new Error("Contract not loaded");

        const totalLogs = await contract.logCount();  // ✅ Check if function exists
        if (!totalLogs) {
            setLogs([]);
            return;
        }

        let logsArray = [];
        for (let i = 0; i < totalLogs; i++) {
            const log = await contract.getLog(i);
            logsArray.push({
                timestamp: new Date(log[0] * 1000).toLocaleString(),
                hash: log[1],
                type: log[2],
            });
        }
        setLogs(logsArray);
    } catch (error) {
        console.error("❌ Error fetching logs:", error.message);
    }
  };

  const addLog = async () => {
    if (!eventType || !details) {
        alert("Enter both event type and details.");
        return;
    }
    try {
        const contract = await getContract();  // ✅ Ensure contract is loaded
        if (!contract) throw new Error("Contract not loaded");

        console.log("🟢 Adding log:", { eventType, details });
        const txn = await contract.addLog(details, eventType);
        await txn.wait();
        alert("✅ Log added successfully");
        setEventType("");
        setDetails("");
        fetchLogs();
    } catch (error) {
        console.error("❌ Error adding log:", error.message);
        alert("Failed to add log: " + error.message);
    }
  };

  return (
    <div className="container">
      <h1>Blockchain Security Logging</h1>

      {account ? (
        <p>Connected Wallet: {account}</p>
      ) : (
        <button onClick={connectWallet}>Connect MetaMask</button> 
      )}

      <div>
        <input type="text" placeholder="Event Type" value={eventType} onChange={(e) => setEventType(e.target.value)} />
        <input type="text" placeholder="Details" value={details} onChange={(e) => setDetails(e.target.value)} />
        <button onClick={addLog}>Add Log</button>
      </div>

      <h2>Stored Logs</h2>
      {logs.length === 0 ? (
        <p>No logs found.</p>
      ) : (
        <ul>
          {logs.map((log, index) => (
            <li key={index}>
              <b>{log.type}</b> - {log.timestamp}
              <br />
              Hash: {log.hash}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;