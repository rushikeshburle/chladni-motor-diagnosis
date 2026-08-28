import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Diagnosis from './pages/Diagnosis'
import Results from './pages/Results'
import History from './pages/History'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col relative">
        {/* Vibration Wave Background */}
        <div className="vibration-waves">
          <div className="vibration-wave" />
          <div className="vibration-wave" />
          <div className="vibration-wave" />
        </div>
        
        <Navbar />
        <main className="flex-1 relative z-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/diagnosis" element={<Diagnosis />} />
            <Route path="/results" element={<Results />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
