// src/AppRouter.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import ScanPage from './ScanPage';
import NavigationPage from './Navigation';
import Home from './Home';

function AppRouter() {
  return (
    <Router>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/scan" element={<ScanPage />} />
      <Route path="/navigate" element={<NavigationPage />} />
    </Routes>
  </Router>
  );
}

export default AppRouter;