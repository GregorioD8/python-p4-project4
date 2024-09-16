import React, { useState, useEffect } from 'react';
import '../index.css'; // Ensure this file is imported for the custom styles

function Home() {
  const [coaches, setCoaches] = useState([]);
  const [showCoaches, setShowCoaches] = useState(false);

  useEffect(() => {
    // Fetch the coaches from your backend API
    fetch('http://127.0.0.1:5000/coaches')
      .then(response => response.json())
      .then(data => setCoaches(data))
      .catch(error => console.error('Error fetching coaches:', error));
  }, []);

  const toggleCoachesList = () => {
    setShowCoaches(!showCoaches);
  };

  // Mapping of coach names to their respective image paths
  const coachImages = {
    "Matilda Hubert": "/images/coaches/1.jpeg",
    "Ricky Milton": "/images/coaches/2.jpeg",
    "Sam Morton": "/images/coaches/3.jpeg",
    "Denise Lawson": "/images/coaches/4.jpeg",
    "Natalie Ventura": "/images/coaches/5.jpeg",
    "Veronica Bolton": "/images/coaches/6.jpeg",
  };

  return (
    <div className="home-page">
      {/* Hero Section */}
      <header className="hero-section text-center">
        <div className="container">
          <img src="/Etherheal_logo.jpg" alt="Etherheal Logo" className="img-fluid mb-4" style={{ maxWidth: "200px" }} />
          <h1 className="display-4">Welcome to Etherheal</h1>
          <p className="lead">Your journey to mental well-being starts here</p>
          <button onClick={toggleCoachesList} className="get-started-btn">
            {showCoaches ? 'Hide Coaches' : 'Get Started'}
          </button>
        </div>
      </header>

      {/* Coaches List */}
      {showCoaches && (
        <section className="coaches-section py-5">
          <div className="container">
            <h2 className="text-center mb-4">Meet Our Coaches</h2>
            <div className="row">
              {coaches.map((coach) => (
                <div key={coach.id} className="col-md-4">
                  <div className="card mb-4">
                    <img
                      src={coachImages[coach.name] || "/images/coaches/default.jpeg"} // Use mapped image or fallback
                      alt={coach.name}
                      className="card-img-top"
                      style={{ objectFit: "cover", height: "200px", width: "100%" }}
                    />
                    <div className="card-body">
                      <h5 className="card-title">{coach.name}</h5>
                      <p className="card-text">{coach.specialization}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="features-section py-5">
        <div className="container">
          <div className="row text-center">
            <div className="col-md-4">
              <i className="bi bi-heart-fill text-primary mb-3" style={{ fontSize: '3rem' }}></i>
              <h3>Personalized Coaching</h3>
              <p>Receive customized guidance tailored to your unique needs.</p>
            </div>
            <div className="col-md-4">
              <i className="bi bi-people-fill text-primary mb-3" style={{ fontSize: '3rem' }}></i>
              <h3>Community Support</h3>
              <p>Join a community of like-minded individuals.</p>
            </div>
            <div className="col-md-4">
              <i className="bi bi-journal-text text-primary mb-3" style={{ fontSize: '3rem' }}></i>
              <h3>Comprehensive Resources</h3>
              <p>Access a wide range of resources to support your journey.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="text-white text-center py-4">
        <div className="container">
          <p>&copy; 2024 Etherheal. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default Home;