import React from 'react';
import { useNavigate } from 'react-router-dom';
 // Ensure you have this CSS file for additional styles

const Home = () => {
  const navigate = useNavigate();

  const openCamera = () => {
    navigate('/scan');
  };

  return (
    <div className="content">
      <div className="logo-container">
        <img src="/logo.png" alt="RSET Navigator Logo" />
      </div>
      <button className="scan-button" onClick={openCamera}>Scan QR Code</button>
    </div>
  );
};

export default Home;