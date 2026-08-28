import React, { useRef } from 'react'
import { Upload, X, Video } from 'lucide-react'

function VideoUploader({ onData, data }) {
  const fileInputRef = useRef(null)

  const handleFileSelect = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload/video', {
        method: 'POST',
        body: formData
      })

      const result = await response.json()
      if (result.success) {
        onData(result)
      }
    } catch (error) {
      console.error('Upload failed:', error)
    }
  }

  const handleRemove = () => {
    onData(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="card hover:scale-105 hover:shadow-xl transition-all duration-300">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2563EB]/10 to-[#06B6D4]/10 flex items-center justify-center border border-[#06B6D4]/20">
          <Video className="w-5 h-5 text-[#2563EB]" />
        </div>
        <h2 className="text-xl font-bold font-heading text-[#0F172A]">Video Analysis</h2>
      </div>

      {!data ? (
        <div 
          className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center hover:border-[#06B6D4] hover:bg-[#06B6D4]/5 transition-all duration-300 cursor-pointer group"
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="w-16 h-16 rounded-full bg-[#F5F8FC] flex items-center justify-center mx-auto mb-4 group-hover:scale-110 group-hover:bg-[#2563EB]/10 transition-transform duration-300">
            <Upload className="w-8 h-8 text-[#2563EB]" />
          </div>
          <p className="text-[#0F172A] mb-2 font-medium font-heading">Drag & Drop</p>
          <p className="text-sm text-gray-500 mb-4">Upload Motor Vibration Video</p>
          <button className="btn-primary text-sm py-2 px-4">
            Browse Video
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative rounded-xl overflow-hidden bg-black/5">
            <video
              src={`http://localhost:8000/api/upload/file/${data.filename}`}
              className="w-full h-48 object-cover"
              controls
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
            <button
              onClick={handleRemove}
              className="absolute top-3 right-3 p-2 bg-red-600/80 backdrop-blur-sm rounded-full hover:bg-red-600 transition-colors"
            >
              <X className="w-4 h-4 text-white" />
            </button>
          </div>
          <div className="glass-card p-4 space-y-2">
            <span className="text-sm text-gray-600">{data.original_filename}</span>
            <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">
              <div>Size: {(data.file_size / (1024*1024)).toFixed(2)} MB</div>
              <div>{data.duration.toFixed(1)}s</div>
              <div>{data.frame_count} frames</div>
              <div>{data.fps.toFixed(1)} FPS</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default VideoUploader
