import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Activity, Home, History, Menu, X, Cpu } from 'lucide-react'
import { useState } from 'react'

function Navbar() {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/diagnosis', label: 'Diagnosis', icon: Activity },
    { path: '/history', label: 'History', icon: History },
  ]
  
  return (
    <nav className="glass-card sticky top-0 z-50 border-b border-gray-200 backdrop-blur-xl">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Activity className="w-10 h-10 text-[#2563EB] animate-pulse-glow" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-[#22C55E] rounded-full animate-pulse" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-heading gradient-text">Chladni Pattern Analysis</h1>
              <p className="text-xs text-gray-500">Motor Vibration Fault Diagnosis</p>
            </div>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl transition-all duration-300 ${
                    isActive
                      ? 'bg-[#2563EB] text-white shadow-lg shadow-[#2563EB]/20 transform scale-105'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-[#2563EB]'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium font-heading">{item.label}</span>
                </Link>
              )
            })}
          </div>

          {/* System Status */}
          <div className="hidden md:flex items-center space-x-3 px-4 py-2 bg-[#22C55E]/10 rounded-xl border border-[#22C55E]/20">
            <div className="w-2 h-2 bg-[#22C55E] rounded-full animate-pulse" />
            <span className="text-sm font-medium text-[#22C55E]">System Online</span>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 glass-card rounded-lg"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6 text-[#0F172A]" /> : <Menu className="w-6 h-6 text-[#0F172A]" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 space-y-2 animate-slide-up">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                    isActive
                      ? 'bg-[#2563EB] text-white'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium font-heading">{item.label}</span>
                </Link>
              )
            })}
            <div className="flex items-center space-x-3 px-4 py-3 bg-[#22C55E]/10 rounded-xl border border-[#22C55E]/20">
              <div className="w-2 h-2 bg-[#22C55E] rounded-full animate-pulse" />
              <span className="text-sm font-medium text-[#22C55E]">System Online</span>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
