import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "./AuthContext";
import SessionForm from "./SessionForm";
import Calendar from "./Calendar";
import '../index.css';  // Corrected import for the CSS file

const CoachDashboard = ({ clients }) => {
  const { coachId } = useContext(AuthContext);
  const [sessions, setSessions] = useState([]);
  const [selectedClient, setSelectedClient] = useState("");
  const [refreshPage, setRefreshPage] = useState(false);

  useEffect(() => {
    if (coachId) {
      const url = selectedClient
        ? `http://127.0.0.1:5000/coaches/${coachId}/sessions?client_id=${selectedClient}`
        : `http://127.0.0.1:5000/coaches/${coachId}/sessions`;

      fetch(url)
        .then(res => res.json())
        .then(data => setSessions(data))
        .catch(error => console.error("Error fetching sessions:", error));
    }
  }, [coachId, selectedClient, refreshPage]);

  const handleClientChange = e => {
    setSelectedClient(e.target.value);
  };

  const handleUpdateNotes = sessionId => {
    const newNotes = prompt("Enter new notes:");
    if (!newNotes || newNotes.trim() === "") {
      alert("Notes cannot be empty.");
      return;
    }
    fetch(`http://127.0.0.1:5000/sessions/${sessionId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ notes: newNotes }),
    })
      .then(res => res.json())
      .then(() => setRefreshPage(!refreshPage));
  };

  const handleDeleteSession = sessionId => {
    fetch(`http://127.0.0.1:5000/sessions/${sessionId}`, {
      method: "DELETE",
    }).then(res => {
      if (res.status === 204) {
        setRefreshPage(!refreshPage);
      } else {
        console.error("Failed to delete session");
      }
    });
  };

  // Submit button style to match the update button
  const submitButtonStyle = {
    padding: "10px 15px",
    backgroundColor: "#468B90", // Match this to the Update button's color
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    fontSize: "16px",
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Coach Dashboard</h1>

      {/* Client Select Dropdown */}
      <div className="row">
        <div className="col-md-4 mb-3">
          <label htmlFor="clientSelect" className="form-label">Select Client</label>
          <select
            id="clientSelect"
            className="form-select"
            onChange={handleClientChange}
            value={selectedClient}
          >
            <option value="" label="All Clients" />
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* grid for the form */}
      <div className="row">
        <div className="col-md-5"> 
          <h2>Schedule a New Session</h2>
          <SessionForm
            onSubmitSuccess={() => setRefreshPage(!refreshPage)}
            selectedCoach={coachId}
            selectedClient={selectedClient}
            clients={clients}
            submitButtonStyle={submitButtonStyle} 
          />
        </div>
        <div className="col-md-7"> {/*calendar width */}
          <h2>Session Calendar</h2>
          <Calendar sessions={sessions} />
        </div>
      </div>

      {/* Sessions Table */}
      <h2 className="mt-4">Scheduled Sessions</h2>
      <div className="table-responsive" style={{ maxHeight: "300px", overflowY: "scroll" }}>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Client Name</th>
              <th>Time</th>
              <th>Notes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sessions.length === 0 ? (
              <tr>
                <td colSpan="4">No sessions scheduled.</td>
              </tr>
            ) : (
              sessions.map((session, i) => (
                <tr key={i}>
                  <td>{session.client_name}</td>
                  <td>{session.date.split(" ")[0]} {session.date.split(" ")[1]}</td>
                  <td>{session.notes}</td>
                  <td>
                    <button className="btn btn-primary" onClick={() => handleUpdateNotes(session.id)}>
                      Update
                    </button>
                    <button className="btn btn-danger ms-2" onClick={() => handleDeleteSession(session.id)}>
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CoachDashboard;