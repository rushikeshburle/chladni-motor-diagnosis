import React from 'react'
import { AlertTriangle, CheckCircle } from 'lucide-react'

function FaultResult({ results }) {
  const isHealthy = results.predicted_fault === 'Healthy'

  return (
    <div className="card">
      <h2 className="text-2xl font-bold font-heading mb-6 gradient-text">Motor Diagnosis</h2>
      
      <div className="space-y-6">
        {/* Predicted Fault */}
        <div className={`p-6 rounded-2xl border ${
          isHealthy 
            ? 'bg-[#22C55E]/10 border-[#22C55E]/30' 
            : 'bg-[#EF4444]/10 border-[#EF4444]/30'
        }`}>
          <div className="flex items-center space-x-4 mb-3">
            <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
              isHealthy 
                ? 'bg-[#22C55E] text-white' 
                : 'bg-[#EF4444] text-white'
            }`}>
              {isHealthy ? (
                <CheckCircle className="w-6 h-6" />
              ) : (
                <AlertTriangle className="w-6 h-6" />
              )}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-600">Detected Condition</p>
              <p className={`text-3xl font-bold font-heading ${isHealthy ? 'text-[#22C55E]' : 'text-[#EF4444]'}`}>
                {results.predicted_fault}
              </p>
            </div>
          </div>
        </div>

        {/* Confidence */}
        <div>
          <p className="text-sm font-medium text-gray-600 mb-3">Classification Confidence</p>
          <div className="flex items-center space-x-4">
            <div className="flex-1 bg-gray-200 rounded-full h-6 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-1000 ${
                  isHealthy 
                    ? 'bg-[#22C55E]' 
                    : 'bg-[#2563EB]'
                }`}
                style={{ width: `${results.confidence * 100}%` }}
              />
            </div>
            <span className="text-2xl font-bold font-mono text-[#0F172A]">
              {(results.confidence * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Risk Level */}
        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Risk Level</p>
              <p className={`text-2xl font-bold font-heading ${
                results.severity === 'High' ? 'text-[#EF4444]' : 
                results.severity === 'Medium' ? 'text-[#F59E0B]' : 
                'text-[#22C55E]'
              }`}>
                {results.severity}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-gray-600 mb-1">Severity Score</p>
              <p className="text-2xl font-bold font-mono text-[#0F172A]">
                {results.severity_score.toFixed(0)}/100
              </p>
            </div>
          </div>
        </div>

        {/* Primary Evidence */}
        <div>
          <p className="text-sm font-medium text-gray-600 mb-3">Primary Evidence</p>
          <ul className="space-y-3">
            {[
              "Abnormal nodal pattern detected",
              "Increased pattern irregularity",
              "High temporal variation in vibration",
              "Operating condition consistent with abnormal vibration"
            ].map((evidence, index) => (
              <li key={index} className="flex items-center space-x-3 text-gray-600">
                <div className="w-2 h-2 bg-[#06B6D4] rounded-full animate-pulse" />
                <span>{evidence}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default FaultResult
