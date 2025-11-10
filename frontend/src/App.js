// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Home from './pages/Home';
import Calculator from './pages/Calculator';
// import './App.css'; // Если не создавали App.css, можно убрать

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App bg-wb-dark text-wb-light min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/calculator" element={<Calculator />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;