```jsx
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { RotateCcw, Zap, AlertTriangle, Cpu } from 'lucide-react'
import ImageUploader from '../components/ImageUploader'
import VideoUploader from '../components/VideoUploader'
import TextInput from '../components/TextInput'
import ProcessingStatus from '../components/ProcessingStatus'

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  'https://chladni-motor-diagnosis-1.onrender.com'

function Diagnosis() {
  const navigate = useNavigate()

  const [imageData, setImageData] = useState(null)
  const [videoData, setVideoData] = useState(null)
  const [textData, setTextData] = useState('')

  const [motorInfo, setMotorInfo] = useState({
    motorId: '',
    motorType: '',
    rpm: '',
    load: '',
    temperature: ''
  })

  const [isProcessing, setIsProcessing] = useState(false)
  const [processingSteps, setProcessingSteps] = useState([])
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!imageData && !videoData && !textData.trim()) {
      setError('Please provide at least one input (image, video, or text)')
      return
    }

    setIsProcessing(true)
    setError(null)
    setProcessingSteps(['Initializing diagnosis...'])

    try {
      setProcessingSteps(prev => [
        ...prev,
        'Validating inputs...'
      ])

      const requestData = {
        motor_id: motorInfo.motorId || null,
        motor_type: motorInfo.motorType || null,
        rpm: motorInfo.rpm ? parseFloat(motorInfo.rpm) : null,
        load: motorInfo.load ? parseFloat(motorInfo.load) : null,
        temperature: motorInfo.temperature
          ? parseFloat(motorInfo.temperature)
          : null,

        image_path: imageData?.file_path || null,
        video_path: videoData?.file_path || null,
        text_input: textData.trim() || null,

        demo_mode: true
      }

      setProcessingSteps(prev => [
        ...prev,
        'Connecting to diagnosis server...'
      ])

      const response = await fetch(
        `${API_BASE_URL}/api/diagnosis/analyze`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        }
      )

      if (!response.ok) {
        throw new Error(
          `Server error: ${response.status} ${response.statusText}`
        )
      }

      const result = await response.json()

      if (result.success) {
        setProcessingSteps(prev => [
          ...prev,
          'Analysis complete!',
          'Generating results...'
        ])

        sessionStorage.setItem(
          'diagnosisResults',
          JSON.stringify(result)
        )

        setTimeout(() => {
          navigate('/results')
        }, 1000)
      } else {
        throw new Error(
          result.error || 'Diagnosis analysis failed'
        )
      }

    } catch (err) {
      console.error('Diagnosis error:', err)

      setError(
        err.message ||
        'Failed to connect to diagnosis server'
      )

      setProcessingSteps(prev => [
        ...prev,
        `Error: ${err.message}`
      ])
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = () => {
    setImageData(null)
    setVideoData(null)
    setTextData('')

    setMotorInfo({
      motorId: '',
      motorType: '',
      rpm: '',
      load: '',
      temperature: ''
    })

    setError(null)
    setProcessingSteps([])
  }

  if (isProcessing) {
    return <ProcessingStatus steps={processingSteps} />
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-slide-up">

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold font-heading gradient-text mb-2">
            Motor Vibration Diagnosis
          </h1>

          <p className="text-gray-500">
            Upload vibration patterns and motor information for AI-powered analysis
          </p>
        </div>

        <button
          onClick={handleReset}
          className="btn-secondary flex items-center space-x-2"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Reset</span>
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-6 py-4 rounded-xl backdrop-blur-sm">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Motor Information */}
      <div className="card">

        <h2 className="text-2xl font-bold font-heading mb-6 gradient-text flex items-center space-x-2">
          <Cpu className="w-6 h-6 text-[#2563EB]" />
          <span>Motor Information</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">

          {[
            {
              key: 'motorId',
              label: 'Motor ID',
              placeholder: 'M-001'
            },
            {
              key: 'motorType',
              label: 'Motor Type',
              placeholder: 'Induction Motor'
            },
            {
              key: 'rpm',
              label: 'RPM',
              placeholder: '1450',
              type: 'number'
            },
            {
              key: 'load',
              label: 'Load (%)',
              placeholder: '75',
              type: 'number'
            },
            {
              key: 'temperature',
              label: 'Temperature (°C)',
              placeholder: '65',
              type: 'number'
            }
          ].map(field => (
            <div key={field.key}>

              <label className="block text-sm font-medium text-gray-600 mb-2">
                {field.label}
              </label>

              <input
                type={field.type || 'text'}
                value={motorInfo[field.key]}
                onChange={e =>
                  setMotorInfo({
                    ...motorInfo,
                    [field.key]: e.target.value
                  })
                }
                className="input-field"
                placeholder={field.placeholder}
              />

            </div>
          ))}

        </div>
      </div>

      {/* Input Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <ImageUploader
          onData={setImageData}
          data={imageData}
        />

        <VideoUploader
          onData={setVideoData}
          data={videoData}
        />

        <TextInput
          onData={setTextData}
          data={textData}
        />

      </div>

      {/* Analyze */}
      <div className="flex justify-center">

        <button
          onClick={handleAnalyze}
          className="btn-primary px-12 py-4 text-xl font-bold font-heading shadow-2xl shadow-[#2563EB]/30 hover:shadow-[#2563EB]/50 animate-pulse-glow"
          disabled={isProcessing}
        >
          Analyze Motor
        </button>

      </div>

      {/* Demo Notice */}
      <div className="glass-card p-6 border border-[#F59E0B]/30">

        <div className="flex items-start space-x-3">

          <div className="w-10 h-10 rounded-full bg-[#F59E0B]/10 flex items-center justify-center flex-shrink-0">
            <Zap className="w-5 h-5 text-[#F59E0B]" />
          </div>

          <div>

            <p className="font-bold text-[#F59E0B] mb-1">
              Demo Mode Active
            </p>

            <p className="text-sm text-gray-500">
              Predictions are generated using demonstration logic.
              Connect a trained model for validated diagnosis.
            </p>

          </div>

        </div>

      </div>

    </div>
  )
}

export default Diagnosis
```
