import React, { useState, useEffect } from "react";
import SessionForm from "./SessionForm";

const CoachDashboard = () => {
  const [sessions, setSessions] = useState([]);
  const [coaches, setCoaches] = useState([]);
  const [clients, setClients] = useState([]);
  const [selectedCoach, setSelectedCoach] = useState("");
  const [selectedClient, setSelectedClient] = useState("");
  const [refreshPage, setRefreshPage] = useState(false);

  // Fetch all coaches when the component mounts
  useEffect(() => {
    fetch("http://127.0.0.1:5000/coaches")
      .then((response) => response.json())
      .then((data) => setCoaches(data))
      .catch((error) => console.error("Error fetching coaches:", error));
  }, []);

  // Fetch clients when a coach is selected
  useEffect(() => {
    if (selectedCoach) {
      fetch(`http://127.0.0.1:5000/coaches/${selectedCoach}/clients`)
        .then((res) => res.json())
        .then((data) => {
          console.log("Fetched clients:", data); // Debugging log
          if (data.length > 0) {
            setClients(data);
          } else {
            setClients([]);  // Clear clients if none found
          }
          setSelectedClient(""); // Reset selected client
        })
        .catch((error) => console.error("Error fetching clients:", error));
    } else {
      setClients([]); // Clear clients if no coach is selected
    }
  }, [selectedCoach]);

  // Fetch sessions based on selected coach and client
  useEffect(() => {
    if (selectedCoach) {
      const url = selectedClient
        ? `http://127.0.0.1:5000/coaches/${selectedCoach}/sessions?client_id=${selectedClient}`
        : `http://127.0.0.1:5000/coaches/${selectedCoach}/sessions`;

      fetch(url)
        .then((res) => res.json())
        .then((data) => setSessions(data))
        .catch((error) => console.error("Error fetching sessions:", error));
    }
  }, [selectedCoach, selectedClient, refreshPage]);

  // Handle coach selection change
  const handleCoachChange = (e) => {
    setSelectedCoach(e.target.value);
    setSessions([]);
    setSelectedClient(""); // Reset client selection when coach changes
  };

  // Handle client selection change
  const handleClientChange = (e) => {
    setSelectedClient(e.target.value);
  };

  // Handle updating session notes
  const handleUpdateNotes = (sessionId) => {
    const newNotes = prompt("Enter new notes:");
    // Validation: Check if the input is empty
    if (!newNotes || newNotes.trim() === "") {
      alert("Notes cannot be empty.");
      return; // Exit the function if the input is invalid
    }
    // Proceed with the update if validation passes
    fetch(`http://127.0.0.1:5000/sessions/${sessionId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ notes: newNotes }),
    })
      .then((res) => res.json())
      .then(() => setRefreshPage(!refreshPage));
  };


  // Handle deleting a session
  const handleDeleteSession = (sessionId) => {
    fetch(`http://127.0.0.1:5000/sessions/${sessionId}`, {
      method: "DELETE",
    }).then((res) => {
      if (res.status === 204) {
        setRefreshPage(!refreshPage);
      } else {
        console.error("Failed to delete session");
      }
    });
  };

  return (
    <div>
      <h1>Coach Dashboard</h1>

      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <label htmlFor="coachSelect">Select Coach</label>
        <select id="coachSelect" onChange={handleCoachChange} value={selectedCoach}>
          <option value="" label="Select coach" />
          {coaches.map((coach) => (
            <option key={coach.id} value={coach.id}>
              {coach.name}
            </option>
          ))}
        </select>

        {clients.length > 0 ? (
          <>
            <label htmlFor="clientSelect">Select Client</label>
            <select id="clientSelect" onChange={handleClientChange} value={selectedClient}>
              <option value="" label="All Clients" />
              {clients.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.name}
                </option>
              ))}
            </select>
          </>
        ) : (
          <p>No clients available for this coach.</p>
        )}
      </div>

      {selectedCoach && (
        <SessionForm
          onSubmitSuccess={() => setRefreshPage(!refreshPage)}
          selectedCoach={selectedCoach}
          selectedClient={selectedClient}
        />
      )}

      {selectedCoach && (
        <>
          <h2>Scheduled Sessions {coaches.find(c => c.id === selectedCoach)?.name}</h2>
          <table style={{ padding: "15px" }}>
            <thead>
              <tr>
                <th>Client Name</th>
                <th>Time</th>
                <th>Notes</th>
  
              </tr>
            </thead>
            <tbody>
              {sessions.length === 0 ? (
                <tr>
                  <td colSpan="5">No sessions scheduled.</td>
                </tr>
              ) : (
                sessions.map((session, i) => (
                  <tr key={i}>
                    <td>{session.client_name}&nbsp;&nbsp;</td>
                    <td>{`${session.date.split(' ')[0]} ${session.date.split(' ')[1]}`}&nbsp;&nbsp;</td>
                    <td>{session.notes}&nbsp;&nbsp;</td>
                    <td>
                      <button onClick={() => handleUpdateNotes(session.id)}>Update</button>
                    </td>
                    <td>
                      <button onClick={() => handleDeleteSession(session.id)}>Delete</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
};

export default CoachDashboard;