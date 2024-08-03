import React, { useState } from "react";

function Coaches({ coaches }) {
  const [selectedCoach, setSelectedCoach] = useState(null);

  return (
    <div>
      <h1>Coaches</h1>
      {selectedCoach ? (
        <div>
          <h2>{selectedCoach.name}</h2>
          <p>{selectedCoach.specialization}</p>
          <button onClick={() => setSelectedCoach(null)}>Back</button>
        </div>
      ) : (
        <ul>
          {coaches.map(coach => (
            <li key={coach.id}>
              {coach.name} <button onClick={() => setSelectedCoach(coach)}>View</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Coaches;