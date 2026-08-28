import React from 'react'
import { AlertTriangle, Shield, CheckCircle } from 'lucide-react'

function SeverityCard({ results }) {
  const score = results.severity_score

  const getSeverityConfig = (severity) => {
    switch (severity) {
      case 'High': 
        return { 
          bg: 'bg-[#EF4444]/10', 
          border: 'border-[#EF4444]/30',
          icon: AlertTriangle,
          text: 'text-[#EF4444]'
        }
      case 'Medium': 
        return { 
          bg: 'bg-[#F59E0B]/10', 
          border: 'border-[#F59E0B]/30',
          icon: Shield,
          text: 'text-[#F59E0B]'
        }
      case 'Low': 
        return { 
          bg: 'bg-[#22C55E]/10', 
          border: 'border-[#22C55E]/30',
          icon: CheckCircle,
          text: 'text-[#22C55E]'
        }
      default: 
        return { 
          bg: 'bg-gray-100', 
          border: 'border-gray-300',
          icon: Shield,
          text: 'text-gray-500'
        }
    }
  }

  const config = getSeverityConfig(results.severity)
  const Icon = config.icon

  return (
    <div className="card">
      <h2 className="text-2xl font-bold font-heading mb-6 gradient-text">Severity Assessment</h2>
      
      <div className="space-y-6">
        {/* Gauge Visualization */}
        <div className="flex items-center justify-center">
          <div className="relative w-56 h-56">
            <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="rgba(37, 99, 235, 0.1)"
                strokeWidth="12"
                strokeLinecap="round"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="url(#gradient)"
                strokeWidth="12"
                strokeLinecap="round"
                strokeDasharray={`${(score / 100) * 251.2} 251.2`}
                className="transition-all duration-1000"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#2563EB" />
                  <stop offset="100%" stopColor="#06B6D4" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-4xl font-bold font-mono text-[#0F172A]">{score.toFixed(0)}</span>
              <span className="text-sm text-gray-500">/ 100</span>
            </div>
          </div>
        </div>

        {/* Severity Level */}
        <div className={`text-center p-6 rounded-2xl ${config.bg} border ${config.border}`}>
          <div className="flex items-center justify-center space-x-2 mb-2">
            <Icon className={`w-6 h-6 ${config.text}`} />
            <p className="text-sm font-medium text-gray-600">Severity Level</p>
          </div>
          <p className={`text-3xl font-bold font-heading ${config.text}`}>
            {results.severity}
          </p>
        </div>

        {/* Description */}
        <div className="glass-card p-4">
          <p className="text-sm text-gray-600">
            {results.severity === 'High' && (
              "Strong abnormal pattern detected. Immediate maintenance investigation recommended."
            )}
            {results.severity === 'Medium' && (
              "Noticeable abnormality detected. Schedule inspection at next maintenance window."
            )}
            {results.severity === 'Low' && (
              "Minor deviation from healthy pattern. Continue regular monitoring."
            )}
          </p>
        </div>
      </div>
    </div>
  )
}

export default SeverityCard
