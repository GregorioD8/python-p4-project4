import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Clients from "./Clients";
import Coaches from "./Coaches";
import Sessions from "./Sessions";
import Home from "./Home";
import CoachDashboard from "./CoachDashboard";
import Login from "./Login";
import Navbar from "./Navbar";
import PrivateRoute from "./PrivateRoute";

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

  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/login">
          <Login />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/clients">
          <Clients clients={clients} />
        </Route>
        <Route path="/coaches">
          <Coaches coaches={coaches} />
        </Route>
        <Route path="/sessions">
          <Sessions sessions={sessions} clients={clients} coaches={coaches} />
        </Route>
        <PrivateRoute
          path="/coach-dashboard"
          component={() => (
            <CoachDashboard
              clients={clients} 
              sessions={sessions}
              coaches={coaches}
            />
          )}
        />
      </Switch>
    </Router>
  );
}

export default App;