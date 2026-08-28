import React, { useState } from 'react'
import { Eye, ChevronDown, ChevronUp } from 'lucide-react'

function ExplainabilityPanel({ results, heatmapPath }) {
  const [showFeatures, setShowFeatures] = useState(true)
  const [showHeatmap, setShowHeatmap] = useState(true)

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold font-heading gradient-text">Explainable AI Analysis</h2>
        <Eye className="w-5 h-5 text-[#2563EB]" />
      </div>

      <div className="space-y-6">
        {/* Heatmap Section */}
        {heatmapPath && (
          <div>
            <button
              onClick={() => setShowHeatmap(!showHeatmap)}
              className="flex items-center justify-between w-full text-left group"
            >
              <h3 className="font-bold font-heading text-[#0F172A] flex items-center space-x-2">
                <span className="w-2 h-2 bg-[#06B6D4] rounded-full animate-pulse" />
                <span>Visual Explanation (Heatmap)</span>
              </h3>
              {showHeatmap ? (
                <ChevronUp className="w-5 h-5 text-gray-400 group-hover:text-[#2563EB] transition-colors" />
              ) : (
                <ChevronDown className="w-5 h-5 text-gray-400 group-hover:text-[#2563EB] transition-colors" />
              )}
            </button>
            
            {showHeatmap && (
              <div className="mt-4 animate-slide-up">
                <div className="glass-card p-4 rounded-xl">
                  <img
                    src={`http://localhost:8000/api/upload/file/${heatmapPath.split('\\').pop()}`}
                    alt="Explainability heatmap"
                    className="w-full h-64 object-contain rounded-lg"
                  />
                </div>
                <p className="text-sm text-gray-500 mt-3">
                  Regions highlighted in red indicate areas that most influenced the model's prediction.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Feature Importance Section */}
        <div>
          <button
            onClick={() => setShowFeatures(!showFeatures)}
            className="flex items-center justify-between w-full text-left group"
          >
            <h3 className="font-bold font-heading text-[#0F172A] flex items-center space-x-2">
              <span className="w-2 h-2 bg-[#06B6D4] rounded-full animate-pulse" />
              <span>Important Features</span>
            </h3>
            {showFeatures ? (
              <ChevronUp className="w-5 h-5 text-gray-400 group-hover:text-[#2563EB] transition-colors" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-400 group-hover:text-[#2563EB] transition-colors" />
            )}
          </button>
          
          {showFeatures && (
            <div className="mt-4 space-y-3 animate-slide-up">
              {results.important_features && results.important_features.length > 0 ? (
                results.important_features.map((feature, index) => (
                  <div key={index} className="flex items-center justify-between p-4 glass-card rounded-xl hover:bg-[#2563EB]/5 transition-all duration-300">
                    <div className="flex items-center space-x-4">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                        feature.contribution === 'High' ? 'bg-[#EF4444] text-white' :
                        feature.contribution === 'Medium' ? 'bg-[#F59E0B] text-white' :
                        'bg-[#22C55E] text-white'
                      }`}>
                        {index + 1}
                      </div>
                      <div>
                        <p className="font-medium text-[#0F172A]">{feature.feature}</p>
                        <p className="text-sm text-gray-500">Value: {feature.value}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                      feature.contribution === 'High' ? 'bg-[#EF4444]/10 text-[#EF4444] border border-[#EF4444]/30' :
                      feature.contribution === 'Medium' ? 'bg-[#F59E0B]/10 text-[#F59E0B] border border-[#F59E0B]/30' :
                      'bg-[#22C55E]/10 text-[#22C55E] border border-[#22C55E]/30'
                    }`}>
                      {feature.contribution}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No feature importance data available</p>
              )}
            </div>
          )}
        </div>

        {/* Explanation Note */}
        <div className="glass-card p-6 border border-[#06B6D4]/30">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-full bg-[#06B6D4]/10 flex items-center justify-center flex-shrink-0">
              <Eye className="w-5 h-5 text-[#06B6D4]" />
            </div>
            <div>
              <p className="font-bold text-[#06B6D4] mb-2">AI Explainability</p>
              <p className="text-sm text-gray-600">
                This explainability analysis shows which regions and features most influenced the model's prediction. The heatmap highlights areas in the input that the model attended to when making its decision.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExplainabilityPanel
