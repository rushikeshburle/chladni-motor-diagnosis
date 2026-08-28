import React from 'react'
import { Loader2 } from 'lucide-react'

function ProcessingStatus({ steps }) {
  return (
    <div className="max-w-2xl mx-auto">
      <div className="card text-center py-16 animate-slide-up">
        <div className="relative mb-8">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-[#2563EB]/10 to-[#06B6D4]/10 flex items-center justify-center mx-auto animate-pulse-glow border border-[#06B6D4]/30">
            <Loader2 className="w-12 h-12 text-[#2563EB] animate-spin" />
          </div>
          <div className="absolute -top-2 -right-2 w-8 h-8 bg-[#06B6D4] rounded-full flex items-center justify-center animate-bounce">
            <div className="w-4 h-4 bg-white rounded-full" />
          </div>
        </div>
        
        <h2 className="text-3xl font-bold font-heading gradient-text mb-4">Processing Analysis</h2>
        <p className="text-gray-500 mb-10 text-lg">Please wait while we analyze the vibration patterns...</p>
        
        <div className="max-w-md mx-auto space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center space-x-4 text-left animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                index === steps.length - 1 
                  ? 'bg-[#06B6D4] text-white animate-pulse' 
                  : 'bg-[#22C55E] text-white'
              }`}>
                {index === steps.length - 1 ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  '✓'
                )}
              </div>
              <span className={`text-sm ${
                index === steps.length - 1 ? 'text-[#0F172A] font-medium' : 'text-gray-500'
              }`}>
                {step}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ProcessingStatus
