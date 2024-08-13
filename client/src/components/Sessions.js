import React, { useState } from "react";

function Sessions({ sessions, clients, coaches }) {
  const [selectedSession, setSelectedSession] = useState(null);

  const getClientNameById = (id) => {
    const client = clients.find((client) => client.id === id);
    return client ? client.name : "Unknown Client";
  };

  const getCoachNameById = (id) => {
    const coach = coaches.find((coach) => coach.id === id);
    return coach ? coach.name : "Unknown Coach";
  };

  return (
    <div>
      <h1>Sessions</h1>
      {selectedSession ? (
        <div>
          <h2>Session Details</h2>
          <p>Date: {selectedSession.date}</p>
          <p>Notes: {selectedSession.notes}</p>
          <p>Goal Progress: {selectedSession.goal_progress}</p>
          <p>Client: {getClientNameById(selectedSession.client_id)}</p>
          <p>Coach: {getCoachNameById(selectedSession.coach_id)}</p>
          <button onClick={() => setSelectedSession(null)}>Back</button>
        </div>
      ) : (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {sessions.map((session) => (
            <li key={session.id} style={{ marginBottom: "10px" }}>
              <button onClick={() => setSelectedSession(session)}>View</button>
              {` Coach: ${getCoachNameById(session.coach_id)}, Client: ${getClientNameById(session.client_id)}, Date: ${session.date}`}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Sessions;