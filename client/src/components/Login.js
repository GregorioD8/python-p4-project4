import React, { useState, useContext } from 'react';
import { useHistory } from 'react-router-dom';
import { AuthContext } from './AuthContext';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const history = useHistory();
    const { login } = useContext(AuthContext);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Send login data to the backend
        fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }), 
        })
        .then(response => response.json())
        .then(data => {
            // If successful use the login func from AuthContext 
            if (data.message === 'Logged in successfully') {
                // Call login with coach_id and coach_name
                login(data.coach_id, data.coach_name);  
                history.push('/coach-dashboard'); // go to dashboard after login
            } else {
                alert('Invalid credentials');
            }
        });
    };

    return (
        <div className="login-page">
            <div className="container d-flex align-items-center justify-content-center" style={{ minHeight: "100vh" }}>
                <div className="card shadow-sm p-4" style={{ maxWidth: "400px", width: "100%" }}>
                    <h2 className="text-center mb-4">Login</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input 
                                type="text" 
                                className="form-control" 
                                id="username" 
                                value={username} 
                                onChange={(e) => setUsername(e.target.value)} 
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input 
                                type="password" 
                                className="form-control" 
                                id="password" 
                                value={password} 
                                onChange={(e) => setPassword(e.target.value)} 
                            />
                        </div>
                        <button type="submit" className="btn btn-primary w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Login;
