import React, { useState, useEffect } from "react";

function Sessions() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/sessions")
    .then(response => response.json())
    .then(data => setSessions(Array.isArray(data) ? data : []))
    .catch(error => {
      console.error("Error fetching sessions:", error);
      setSessions([]);
    });
  }, []);

  return (
    <div>
      <h1>Sessions</h1>
      {sessions.length > 0 ? (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {sessions.map((session) => (
            <li key={session.id} style={{ marginBottom: "10px" }}>
                {`Coach: ${session.coach_name}, Client: ${session.client_name}, Date: ${session.date}`}
            </li>
          ))}
        </ul>
      ) : (
        <p>No sessions available</p>
      )}
    </div>
  );
}

export default Sessions;