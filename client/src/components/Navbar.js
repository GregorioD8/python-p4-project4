import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from './AuthContext';

function Navbar() {
    const { isAuthenticated, coachName, logout } = useContext(AuthContext);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Home</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        {isAuthenticated && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/coach-dashboard">Dashboard</Link>
                                </li>
                            </>
                        )}
                    </ul>
                    <ul className="navbar-nav">
                        {isAuthenticated ? (
                            <li className="nav-item">
                                <button 
                                    className="btn btn-outline-danger" 
                                    onClick={() => {
                                        logout();
                                        window.location.href = '/login';
                                    }}>
                                    Logout {coachName} {/* coaches name ont the button */}
                                </button>
                            </li>
                        ) : (
                            <li className="nav-item">
                                <Link className="nav-link" to="/login">Login</Link>
                            </li>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;