import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import "./App.css";
import Agent from "./Agent";

function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="landing-container">
      <div className="landing-card">
        <div className="landing-logo">🏡</div>
        <div className="landing-title">AI Real Estate Advisor</div>
        <p className="landing-desc">
          Welcome to <b>AI Real Estate Advisor</b> — your smart, data-driven partner for navigating the San Francisco Bay Area housing market.<br /><br />
          <b>What we offer:</b>
        </p>
        <ul className="landing-list">
          <li>Ask natural language questions about neighborhoods, prices, and trends</li>
          <li>Get up-to-date property listings and market insights</li>
          <li>Visualize data and receive AI-powered advice</li>
          <li>Modern, intuitive interface for home buyers and investors</li>
        </ul>
        <button className="landing-btn" onClick={() => navigate("/agent")}>Try the AI Agent</button>
      </div>
      <div className="landing-footer">
        &copy; {new Date().getFullYear()} AI Real Estate Advisor &mdash; Built for smarter real estate decisions.
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/agent" element={<Agent />} />
      </Routes>
    </Router>
  );
}

export default App;
