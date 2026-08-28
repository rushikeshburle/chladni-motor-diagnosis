import React, { useEffect, useState } from 'react'
import { Trash2, Clock, AlertCircle } from 'lucide-react'

function History() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const response = await fetch('/api/history/')
      const data = await response.json()
      if (data.success) {
        setRecords(data.records)
      } else {
        setError('Failed to load history')
      }
    } catch (err) {
      setError('Failed to connect to server')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (recordId) => {
    if (!confirm('Are you sure you want to delete this record?')) return

    try {
      const response = await fetch(`/api/history/${recordId}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        setRecords(records.filter(r => r.diagnosis_id !== recordId))
      }
    } catch (err) {
      console.error('Delete failed:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading history...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="glass-card p-6 border border-red-200">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <span className="text-red-600">{error}</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-slide-up">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold font-heading gradient-text mb-2">Diagnosis History</h1>
          <p className="text-gray-500">View past motor fault diagnosis records</p>
        </div>
        <div className="glass-card px-4 py-2">
          <span className="text-gray-500">Total: </span>
          <span className="font-bold font-mono text-[#0F172A]">{records.length}</span>
        </div>
      </div>

      {records.length === 0 ? (
        <div className="card text-center py-16">
          <div className="w-20 h-20 rounded-full bg-[#2563EB]/10 flex items-center justify-center mx-auto mb-6">
            <Clock className="w-10 h-10 text-[#2563EB]" />
          </div>
          <h2 className="text-2xl font-bold font-heading text-[#0F172A] mb-4">No Diagnosis Records</h2>
          <p className="text-gray-500 mb-8">Start a new motor diagnosis to see your results here</p>
          <button
            onClick={() => window.location.href = '/diagnosis'}
            className="btn-primary"
          >
            Start New Diagnosis
          </button>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Date</th>
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Motor ID</th>
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Diagnosis</th>
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Confidence</th>
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Severity</th>
                  <th className="text-left px-6 py-4 text-sm font-bold font-heading text-gray-600">Action</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record, index) => (
                  <tr 
                    key={record.diagnosis_id} 
                    className="border-b border-gray-100 hover:bg-[#2563EB]/5 transition-colors animate-slide-up"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(record.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-[#0F172A]">
                      {record.motor_id || 'N/A'}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${
                          record.predicted_fault === 'Healthy' ? 'bg-[#22C55E]' : 'bg-[#EF4444]'
                        }`} />
                        <span className="text-sm font-medium text-[#0F172A]">{record.predicted_fault}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm font-mono text-[#0F172A]">
                      {(record.confidence * 100).toFixed(1)}%
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        record.severity === 'High' ? 'bg-[#EF4444]/10 text-[#EF4444] border border-[#EF4444]/30' :
                        record.severity === 'Medium' ? 'bg-[#F59E0B]/10 text-[#F59E0B] border border-[#F59E0B]/30' :
                        'bg-[#22C55E]/10 text-[#22C55E] border border-[#22C55E]/30'
                      }`}>
                        {record.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleDelete(record.diagnosis_id)}
                        className="p-2 glass-card rounded-lg hover:bg-red-50 hover:border-red-200 transition-all duration-300 group"
                      >
                        <Trash2 className="w-4 h-4 text-gray-400 group-hover:text-red-600 transition-colors" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default History
