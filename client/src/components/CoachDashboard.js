import React, { useState, useEffect } from "react";
import SessionForm from "./SessionForm";

const CoachDashboard = () => {
  const [sessions, setSessions] = useState([]);
  const [coaches, setCoaches] = useState([]); // State for storing coaches
  const [selectedCoach, setSelectedCoach] = useState("");
  const [refreshPage, setRefreshPage] = useState(false);

  useEffect(() => {
    // Fetch coaches
    fetch("http://127.0.0.1:5000/coaches")
      .then((response) => response.json())
      .then((data) => setCoaches(data))
      .catch((error) => console.error("Error fetching coaches:", error));
  }, []);

  useEffect(() => {
    if (selectedCoach) {
      fetch(`http://127.0.0.1:5000/coaches/${selectedCoach}/sessions`)
        .then((res) => res.json())
        .then((data) => setSessions(data))
        .catch((error) => console.error("Error fetching sessions:", error));
    }
  }, [selectedCoach, refreshPage]);

  const handleCoachChange = (e) => {
    setSelectedCoach(e.target.value);
    setSessions([]); // Clear sessions when a different coach is selected
  };

  return (
    <div>
      <h1>Coach Dashboard</h1>

      <label htmlFor="coachSelect">Select Coach</label>
      <br />
      <select
        id="coachSelect"
        onChange={handleCoachChange}
        value={selectedCoach}
      >
        <option value="" label="Select coach" />
        {coaches.map((coach) => (
          <option key={coach.id} value={coach.id}>
            {coach.name}
          </option>
        ))}
      </select>

      {selectedCoach && (
        <SessionForm
          onSubmitSuccess={() => setRefreshPage(!refreshPage)}
          selectedCoach={selectedCoach} // Pass the selected coach to the form
        />
      )}

      {selectedCoach && (
        <>
          <h2>Scheduled Sessions for {coaches.find(c => c.id === selectedCoach)?.name}</h2>
          <table style={{ padding: "15px" }}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Client Name</th>
              </tr>
            </thead>
            <tbody>
              {sessions.length === 0 ? (
                <tr>
                  <td colSpan="3">No sessions scheduled.</td>
                </tr>
              ) : (
                sessions.map((session, i) => (
                  <tr key={i}>
                    <td>{session.date}</td>
                    <td>{session.time}</td>
                    <td>{session.clientName}</td>
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