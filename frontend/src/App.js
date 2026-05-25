import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState({
    total_records: 0,
    approved: 0,
    flagged: 0
  });

  const [records, setRecords] = useState([]);
  const [file, setFile] = useState(null);
  const [sourceType, setSourceType] = useState("SAP");

  useEffect(() => {
    loadDashboard();
    loadRecords();
  }, []);

  const loadDashboard = () => {
    fetch("http://127.0.0.1:8000/api/dashboard/")
      .then((response) => response.json())
      .then((result) => setData(result));
  };

  const loadRecords = () => {
    fetch("http://127.0.0.1:8000/api/records/")
      .then((response) => response.json())
      .then((result) => setRecords(result));
  };

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("source_type", sourceType);

    const response = await fetch("http://127.0.0.1:8000/api/upload/", {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    alert(result.message || result.error || "Upload failed");

    loadDashboard();
    loadRecords();
  };

  const approveRecord = async (id) => {
    const response = await fetch(`http://127.0.0.1:8000/api/approve/${id}/`, {
      method: "POST"
    });

    const result = await response.json();
    alert(result.message || result.error);

    loadDashboard();
    loadRecords();
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial", background: "#f7f9fb", minHeight: "100vh" }}>
      <h1>Breathe ESG Dashboard</h1>
      <p>Prototype for ESG data ingestion, normalization, analyst review, and approval workflow.</p>

      <div style={{ display: "flex", gap: "20px", marginTop: "30px" }}>
        <div style={cardStyle}>
          <h3>Total Records</h3>
          <p>{data.total_records}</p>
        </div>

        <div style={cardStyle}>
          <h3>Approved</h3>
          <p>{data.approved}</p>
        </div>

        <div style={cardStyle}>
          <h3>Flagged</h3>
          <p>{data.flagged}</p>
        </div>
      </div>

      <div style={sectionStyle}>
        <h2>Upload CSV File</h2>

        <label>Source Type: </label>
        <select value={sourceType} onChange={(e) => setSourceType(e.target.value)}>
          <option value="SAP">SAP Fuel / Procurement</option>
          <option value="UTILITY">Utility Electricity</option>
          <option value="TRAVEL">Corporate Travel</option>
        </select>

        <br /><br />

        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />

        <br /><br />

        <button style={buttonStyle} onClick={uploadFile}>Upload</button>
      </div>

      <div style={sectionStyle}>
        <h2>Analyst Review Table</h2>

        <table border="1" cellPadding="10" style={{ borderCollapse: "collapse", width: "100%", background: "white" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Source</th>
              <th>Scope</th>
              <th>Category</th>
              <th>Activity</th>
              <th>Value</th>
              <th>Unit</th>
              <th>Suspicious</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {records.map((record) => (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td>{record.source_type}</td>
                <td>{record.scope}</td>
                <td>{record.category}</td>
                <td>{record.activity_type}</td>
                <td>{record.raw_value}</td>
                <td>{record.raw_unit}</td>
                <td>{record.is_suspicious ? "Yes" : "No"}</td>
                <td>{record.status}</td>
                <td>
                  {record.status !== "APPROVED" ? (
                    <button style={smallButtonStyle} onClick={() => approveRecord(record.id)}>
                      Approve
                    </button>
                  ) : (
                    "Locked"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const cardStyle = {
  border: "1px solid #ddd",
  padding: "20px",
  width: "200px",
  background: "white",
  borderRadius: "8px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
};

const sectionStyle = {
  marginTop: "40px",
  padding: "20px",
  background: "white",
  borderRadius: "8px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
};

const buttonStyle = {
  padding: "10px 20px",
  background: "#1f7a4d",
  color: "white",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};

const smallButtonStyle = {
  padding: "6px 12px",
  background: "#1f7a4d",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer"
};

export default App;