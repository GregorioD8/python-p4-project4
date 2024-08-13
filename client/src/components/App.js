import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Clients from "./Clients";
import Coaches from "./Coaches";
import Sessions from "./Sessions";
import Home from "./Home";
import CoachDashboard from "./CoachDashboard";

function App() {
  const [clients, setClients] = useState([]);
  const [coaches, setCoaches] = useState([]);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/clients")
      .then(response => response.json())
      .then(data => setClients(data))
      .catch(error => console.error("Error fetching clients:", error));

    fetch("http://127.0.0.1:5000/coaches")
      .then(response => response.json())
      .then(data => setCoaches(data))
      .catch(error => console.error("Error fetching coaches:", error));

    fetch("http://127.0.0.1:5000/sessions")
      .then(response => response.json())
      .then(data => setSessions(data))
      .catch(error => console.error("Error fetching sessions:", error));
  }, []);

  const onClientAdded = (newClient) => {
    setClients([...clients, newClient]);
  };

  const onCoachAdded = (newCoach) => {
    setCoaches([...coaches, newCoach]);
  };

  return (
    <Router>
      <nav>
        <Link to="/"> Home </Link> |
        <Link to="/clients"> Clients </Link> | 
        <Link to="/coaches"> Coaches </Link> | 
        <Link to="/sessions"> Sessions </Link> |
        <Link to="/coach-dashboard"> Coach Dashboard </Link>
      </nav>
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/clients">
          <Clients clients={clients} onClientAdded={onClientAdded} />
        </Route>
        <Route path="/coaches">
          <Coaches coaches={coaches} onCoachAdded={onCoachAdded} />
        </Route>
        <Route path="/sessions">
          <Sessions sessions={sessions} clients={clients} coaches={coaches} />
        </Route>
        <Route path="/coach-dashboard" component={CoachDashboard} />
      </Switch>
    </Router>
  );
}

export default App;