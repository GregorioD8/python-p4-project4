import React, { useState } from "react";

function Clients({ clients }) {
  const [selectedClient, setSelectedClient] = useState(null);

  return (
    <div>
      <h1>Clients</h1>
      {selectedClient ? (
        <div>
          <h2>{selectedClient.name}</h2>
          <p>{selectedClient.goals}</p>
          <button onClick={() => setSelectedClient(null)}>Back</button>
        </div>
      ) : (
        <ul>
          {clients.map(client => (
            <li key={client.id}>
              {client.name} <button onClick={() => setSelectedClient(client)}>View</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Clients;