import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Download, AlertTriangle, CheckCircle, FileText, Shield } from 'lucide-react'
import FaultResult from '../components/FaultResult'
import ProbabilityChart from '../components/ProbabilityChart'
import SeverityCard from '../components/SeverityCard'
import ExplainabilityPanel from '../components/ExplainabilityPanel'

function Results() {
  const navigate = useNavigate()
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedResults = sessionStorage.getItem('diagnosisResults')
    if (storedResults) {
      setResults(JSON.parse(storedResults))
      setLoading(false)
    } else {
      navigate('/diagnosis')
    }
  }, [navigate])

  const handleDownloadReport = async () => {
    if (results?.report_path) {
      try {
        const response = await fetch(`/api/upload/file/${results.report_path.split('\\').pop()}`)
        if (response.ok) {
          alert('Report download initiated')
        }
      } catch (error) {
        console.error('Download failed:', error)
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading results...</div>
      </div>
    )
  }

  if (!results) {
    return null
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-slide-up">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/diagnosis')}
            className="p-3 glass-card rounded-xl hover:bg-gray-100 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-[#0F172A]" />
          </button>
          <div>
            <h1 className="text-4xl font-bold font-heading gradient-text mb-1">Motor Diagnosis Result</h1>
            <p className="text-gray-500">Motor fault analysis complete</p>
          </div>
        </div>
        {results.report_path && (
          <button
            onClick={handleDownloadReport}
            className="btn-primary flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Download Report</span>
          </button>
        )}
      </div>

      {/* Demo Mode Banner */}
      {results.demo_mode && (
        <div className="glass-card p-6 border border-[#F59E0B]/30">
          <div className="flex items-start space-x-4">
            <div className="w-12 h-12 rounded-full bg-[#F59E0B]/10 flex items-center justify-center flex-shrink-0">
              <AlertTriangle className="w-6 h-6 text-[#F59E0B]" />
            </div>
            <div>
              <p className="font-bold text-[#F59E0B] mb-2">Demo Mode Prediction</p>
              <p className="text-sm text-gray-500">
                This prediction was generated using demonstration logic. Connect a trained model for validated diagnosis.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Results Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <FaultResult results={results} />
        <SeverityCard results={results} />
      </div>

      {/* Probability Distribution */}
      <div className="card">
        <h2 className="text-2xl font-bold font-heading mb-6 gradient-text">Fault Probability Distribution</h2>
        <ProbabilityChart distribution={results.probability_distribution} />
      </div>

      {/* Explainability Panel */}
      <ExplainabilityPanel 
        results={results}
        heatmapPath={results.heatmap_path}
      />

      {/* Maintenance Recommendation */}
      <div className="card border-l-4 border-l-[#06B6D4]">
        <h2 className="text-2xl font-bold font-heading mb-6 gradient-text flex items-center space-x-2">
          <Shield className="w-6 h-6 text-[#06B6D4]" />
          <span>Recommended Action</span>
        </h2>
        <p className="text-gray-600 mb-6 leading-relaxed">
          {results.severity === 'High' && (
            "Inspect bearing assembly and perform detailed vibration analysis under controlled operating conditions. Consider scheduling immediate maintenance to prevent further damage."
          )}
          {results.severity === 'Medium' && (
            "Schedule inspection at next maintenance window. Monitor vibration levels closely and perform detailed analysis if symptoms persist."
          )}
          {results.severity === 'Low' && (
            "Continue regular monitoring. Minor deviation from healthy pattern detected. No immediate action required."
          )}
        </p>
        <div className="flex flex-wrap gap-3">
          <button className="btn-primary flex items-center space-x-2">
            <FileText className="w-4 h-4" />
            <span>Generate Report</span>
          </button>
          <button className="btn-secondary flex items-center space-x-2">
            <Shield className="w-4 h-4" />
            <span>View Detailed Analysis</span>
          </button>
          <button className="btn-secondary flex items-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Save Diagnosis</span>
          </button>
        </div>
      </div>

      {/* Processing Steps */}
      <div className="card">
        <h2 className="text-2xl font-bold font-heading mb-6 gradient-text flex items-center space-x-2">
          <CheckCircle className="w-6 h-6 text-[#22C55E]" />
          <span>Processing Steps</span>
        </h2>
        <div className="space-y-3">
          {results.processing_steps.map((step, index) => (
            <div key={index} className="flex items-center space-x-4 animate-slide-up" style={{ animationDelay: `${index * 0.05}s` }}>
              <div className="w-8 h-8 rounded-full bg-[#22C55E] text-white flex items-center justify-center text-sm font-bold">
                ✓
              </div>
              <span className="text-gray-600">{step}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Input Information */}
      <div className="card">
        <h2 className="text-2xl font-bold font-heading mb-6 gradient-text">Input Information</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Input Type', value: results.input_type },
            { label: 'Modalities Used', value: results.input_type.replace('+', ', ') },
            { label: 'Confidence', value: `${(results.confidence * 100).toFixed(1)}%` },
            { label: 'Severity', value: results.severity }
          ].map((item, index) => (
            <div key={index} className="glass-card p-4">
              <span className="text-sm text-gray-500 block mb-1">{item.label}</span>
              <p className="font-bold font-mono text-[#0F172A]">{item.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* New Analysis Button */}
      <div className="flex justify-center">
        <button
          onClick={() => navigate('/diagnosis')}
          className="btn-primary px-12 py-4 text-xl font-bold font-heading shadow-2xl shadow-[#2563EB]/30 hover:shadow-[#2563EB]/50 animate-pulse-glow"
        >
          New Analysis
        </button>
      </div>
    </div>
  )
}

export default Results
