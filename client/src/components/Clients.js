import React, { useState } from "react";
import ClientsForm from "./ClientsForm";

function Clients({ clients, onClientAdded }) {
  const [selectedClient, setSelectedClient] = useState(null);

  const handleClientAdded = (newClient) => {
    onClientAdded(newClient);
    setSelectedClient(null);
  };

  return (
    <div>
      <h1>Clients</h1>
      <ClientsForm onSubmitSuccess={handleClientAdded} />
      {selectedClient ? (
        <div>
          <h2>{'Client: ' + selectedClient.name}</h2>
          <p>{'Goals: ' + selectedClient.goals}</p>
          <button onClick={() => setSelectedClient(null)}>Back</button>
        </div>
      ) : (
        <ul>
          {clients.map((client) => (
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