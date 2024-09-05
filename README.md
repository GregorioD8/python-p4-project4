# Phase 5 Flask + React Project

### `What I learned`

- How to build a full-stack web application using Flask for the backend and React for the frontend.
- Integrating Flask with SQLAlchemy as the ORM to interact with a database:
    1. Choose an ORM library: `SQLAlchemy`
    2. Install the ORM library: `pip install flask_sqlalchemy`
    3. Configure the database connection: `app.py --> app.config['SQLALCHEMY_DATABASE_URI']`
    4. Define models and relationships: `Created Python classes to define tables and relationships`
    
# By using an ORM you can interact with your database using Python objects, making it easier to manage complex data models and CRUD operations.

This is the directory structure:

```console
├── client
│   ├── public
│   │   ├── images
│   │   │   ├── coaches: folder to store coach profile images
│   │   └── index.html
│   └── src
│       ├── components
│       │   ├── App.js
│       │   ├── AuthContext.js
│       │   ├── Calendar.js
│       │   ├── Clients.js
│       │   ├── ClientsForm.js
│       │   ├── CoachDashboard.js
│       │   ├── Coaches.js
│       │   ├── CoachesForm.js
│       │   ├── Home.js
│       │   ├── Login.js
│       │   ├── Navbar.js
│       │   ├── PrivateRoute.js
│       │   ├── SessionForm.js
│       │   ├── Sessions.js
│       └── index.js
├── server
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   └── seed.py
└── app.db # SQLite database
```
### `Setup`

# Run cd client to cd into the client folder /client
cd client

# Run npm install to install React dependencies
npm install

# Run npm start to start the frontend React application
npm start

# Navigate to the server folder /server
cd ../server 

# Run python seed.py to seed the database
delete app.db then run python seed.py

# Run flask run to start the Flask backend server
flask run

### `Running the Application`

```console
└── Main Menu (Frontend - React)
    ├── View Coaches
    ├── Log in as a Coach
    └── Schedule a Session (Once logged in)

        └── Coach Dashboard
        ├── View Coach Profile and Sessions
        ├── Schedule new sessions
        └── Update/Delete sessions  
```

## Flask API, React Components, and Class relation 

### Flask API
In the backend, Flask serves as the API layer to handle requests and responses. The key routes are:

1. `/coaches`: 
   - **GET**: Fetches all coaches.
   - **POST**: Creates a new coach.
   
2. `/sessions`: 
   - **GET**: Fetches all sessions.
   - **POST**: Schedules a new session.
   - **PATCH**: Updates session notes.
   - **DELETE**: Deletes a session.
   
3. `/login`: 
   - **POST**: Authenticates the coach by verifying their username and password.

The Flask API interacts with the **SQLite** database via **SQLAlchemy**, which acts as the Object Relational Mapper (ORM). The key models in the database are `Coach`, `Client`, and `Session`, which represent the core data entities.

- **Coach**: 
  Represents a coach in the application,including their name, specialization, and login credentials.
  
- **Client**: 
  Represents a client who works with coaches in various sessions.
  
- **Session**: 
  Represents a scheduled session between a coach and a client, including session notes and progress tracking.

These models are managed in the Flask app using routes that provide CRUD (Create, Read, Update, Delete) functionality to the frontend React components.

### React Components
The frontend is built in **React**, where components correspond to specific parts of the user interface. The React components communicate with the Flask API to retrieve or update data. Here's a brief overview of the main components:

1. **App.js**: 
   - The root component that contains the routing logic for different pages of the app. It integrates with `AuthContext.js` for managing authentication state (e.g., if a coach is logged in or not).

2. **AuthContext.js**: 
   - Manages authentication logic. It stores and provides the login state across components, ensuring that only logged-in users can access certain pages like the Coach Dashboard.

3. **CoachDashboard.js**: 
   - The main dashboard for logged-in coaches. It displays scheduled sessions, allows coaches to add, edit, or delete sessions, and also shows the coach's profile picture.

4. **Coaches.js**: 
   - Displays a list of all coaches, each with a profile picture and specialization. It pulls this data from the Flask API via a `GET` request to the `/coaches` route.

5. **Clients.js**: 
   - Shows a list of clients that the coach is working with. It retrieves client data from the Flask API.

6. **SessionForm.js**: 
   - A form component that allows coaches to schedule new sessions with clients. It sends a `POST` request to the `/sessions` route to save the new session to the database.

7. **Calendar.js**: 
   - Uses a popular calendar library (such as FullCalendar) to render the coach's sessions visually in a calendar format.

8. **Home.js**: 
   - The homepage that includes an introductory section, a “Meet Our Coaches” section, and a call-to-action button to get started by viewing coaches or logging in.

9. **Login.js**: 
   - A form that allows coaches to log into the application. It sends a `POST` request to the `/login` route on the Flask backend to authenticate the coach.

10. **PrivateRoute.js**: 
    - A wrapper for routes that should only be accessible to logged-in users. It checks the authentication state (provided by `AuthContext.js`) and redirects users to the login page if they are not authenticated.

11. **Navbar.js**: 
    - The navigation bar that displays links to different parts of the aplication (e.g., Home, Coach Dashboard, Login). It changes based on whether a user is logged in or not.

12. **ClientsForm.js**: 
    - A form to add a new client to the database. It sends a `POST` request to the Flask backend to save the client information.

### Class Relation
The database entities (i.e., `Coach`, `Client`, and `Session` models) map to their respective components on the front end:

1. **Coach** (Flask model) ↔ **Coaches.js** (React component)
   - The `Coaches` component pulls data about each coach (name, specialization) from the Flask API and displays it, along with an image, to the user.

2. **Session** (Flask model) ↔ **SessionForm.js**, **CoachDashboard.js**, **Calendar.js** (React components)
   - The `SessionForm` allows the coach to create new sessions, which are then stored in the database via the `Session` model.
   - The `CoachDashboard` component retrieves the logged-in coach’s sessions and displays them in a table, and the `Calendar` component provides a visual display of all scheduled sessions.

3. **Client** (Flask model) ↔ **Clients.js**, **ClientsForm.js** (React components)
   - The `Clients` component retrieves and displays all the clients that a coach works with. The `ClientsForm` allows the coach to add new clients.

This relationship between the Flask models and React components helps ensure smooth data flow between the backend (API and database) and frontend (UI).