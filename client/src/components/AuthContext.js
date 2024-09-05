import React, { createContext, useState } from 'react';
// create a context to manage teh authentication state
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('authToken') !== null);
    const [coachId, setCoachId] = useState(localStorage.getItem('coachId') || null);
    const [coachName, setCoachName] = useState(localStorage.getItem('coachName') || '');
    
    //login saves details and updates state
    const login = (id, name) => {
        //save login info
        localStorage.setItem('authToken', true); 
        localStorage.setItem('coachId', id);
        localStorage.setItem('coachName', name); 

        // Update state as authenticated
        setIsAuthenticated(true);
        setCoachId(id);
        setCoachName(name); 
    };
    // Logout function clears details from localStorage and state
    const logout = () => {
        // delete old stored data
        localStorage.removeItem('authToken');
        localStorage.removeItem('coachId');
        localStorage.removeItem('coachName');

        // Reset state
        setIsAuthenticated(false);
        setCoachId(null);
        setCoachName(null);
    };

    return (
        // provides tha authentication state and functions to the rest of app
        <AuthContext.Provider value={{ isAuthenticated, coachId, coachName, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};