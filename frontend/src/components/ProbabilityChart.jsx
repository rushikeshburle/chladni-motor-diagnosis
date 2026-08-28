import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function ProbabilityChart({ distribution }) {
  const data = Object.entries(distribution).map(([fault, probability]) => ({
    fault: fault.replace(' ', '\n'),
    probability: (probability * 100).toFixed(1)
  }))

  return (
    <div className="h-96">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(37, 99, 235, 0.1)" />
          <XAxis 
            type="number" 
            domain={[0, 100]} 
            tickFormatter={(value) => `${value}%`}
            stroke="#9ca3af"
          />
          <YAxis 
            type="category" 
            dataKey="fault" 
            width={130}
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            stroke="#9ca3af"
          />
          <Tooltip 
            formatter={(value) => [`${value}%`, 'Probability']}
            contentStyle={{ 
              backgroundColor: 'rgba(255, 255, 255, 0.95)', 
              border: '1px solid rgba(37, 99, 235, 0.2)',
              borderRadius: '8px',
              color: '#0F172A'
            }}
          />
          <Bar 
            dataKey="probability" 
            fill="url(#barGradient)"
            radius={[0, 8, 8, 0]}
          />
          <defs>
            <linearGradient id="barGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#2563EB" />
              <stop offset="100%" stopColor="#06B6D4" />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default ProbabilityChart
