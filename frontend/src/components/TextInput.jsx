import React from 'react'
import { FileText, X } from 'lucide-react'

function TextInput({ onData, data }) {
  const handleChange = (event) => {
    onData(event.target.value)
  }

  const handleClear = () => {
    onData('')
  }

  return (
    <div className="card hover:scale-105 hover:shadow-xl transition-all duration-300">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2563EB]/10 to-[#06B6D4]/10 flex items-center justify-center border border-[#06B6D4]/20">
          <FileText className="w-5 h-5 text-[#2563EB]" />
        </div>
        <h2 className="text-xl font-bold font-heading text-[#0F172A]">Operating Information</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-2">
            Describe motor operating conditions...
          </label>
          <textarea
            value={data}
            onChange={handleChange}
            placeholder="Enter motor operating conditions, observations, or maintenance notes..."
            className="w-full h-48 px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#06B6D4] text-[#0F172A] placeholder-gray-400 resize-none"
          />
        </div>

        {data && (
          <div className="flex justify-end">
            <button
              onClick={handleClear}
              className="flex items-center space-x-1 text-sm text-gray-500 hover:text-[#2563EB] transition-colors"
            >
              <X className="w-4 h-4" />
              <span>Clear</span>
            </button>
          </div>
        )}

        <div className="glass-card p-3">
          <p className="text-xs text-gray-500">
            Example: "The motor operates at 1450 RPM under 75% load. High vibration is observed near the bearing housing."
          </p>
        </div>
      </div>
    </div>
  )
}

export default TextInput
