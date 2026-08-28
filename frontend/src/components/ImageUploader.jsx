```jsx
import React, { useRef, useState } from 'react'
import {
  Upload,
  X,
  Image as ImageIcon,
  Loader2,
  AlertCircle,
  CheckCircle
} from 'lucide-react'

// LIVE BACKEND
const API_BASE_URL = 'https://chladni-motor-diagnosis-1.onrender.com/api'

function ImageUploader({ onData, data }) {
  const fileInputRef = useRef(null)

  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0]

    if (!file) return

    setError('')

    // Validate image
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file.')
      return
    }

    // Maximum 10 MB
    if (file.size > 10 * 1024 * 1024) {
      setError('Image size must be less than 10 MB.')
      return
    }

    setUploading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(
        `${API_BASE_URL}/upload/image`,
        {
          method: 'POST',
          body: formData
        }
      )

      const result = await response.json()

      if (!response.ok) {
        throw new Error(
          result?.detail ||
          result?.error ||
          `Upload failed. Status: ${response.status}`
        )
      }

      if (!result.success) {
        throw new Error(
          result.error || 'Image upload failed.'
        )
      }

      // Save uploaded image data
      onData(result)

    } catch (err) {
      console.error('Image upload error:', err)

      setError(
        err.message ||
        'Unable to connect to the backend server.'
      )

      onData(null)

    } finally {
      setUploading(false)
    }
  }

  const handleRemove = () => {
    onData(null)
    setError('')

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const imageUrl =
    data?.filename
      ? `${API_BASE_URL}/upload/file/${encodeURIComponent(data.filename)}`
      : null

  return (
    <div className="card hover:scale-105 hover:shadow-xl transition-all duration-300">

      {/* Header */}
      <div className="flex items-center space-x-3 mb-4">

        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#2563EB]/10 to-[#06B6D4]/10 flex items-center justify-center border border-[#06B6D4]/20">

          <ImageIcon className="w-5 h-5 text-[#2563EB]" />

        </div>

        <h2 className="text-xl font-bold font-heading text-[#0F172A]">
          Image Analysis
        </h2>

      </div>

      {/* Error */}
      {error && (
        <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 text-sm flex items-start gap-2">

          <AlertCircle className="w-5 h-5 flex-shrink-0" />

          <span>{error}</span>

        </div>
      )}

      {!data ? (

        /* Upload Section */
        <div
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 ${
            uploading
              ? 'border-[#2563EB] bg-[#2563EB]/5 cursor-wait'
              : 'border-gray-300 hover:border-[#06B6D4] hover:bg-[#06B6D4]/5 cursor-pointer'
          }`}
          onClick={() => {
            if (!uploading) {
              fileInputRef.current?.click()
            }
          }}
        >

          {/* Upload Icon */}
          <div className="w-16 h-16 rounded-full bg-[#F5F8FC] flex items-center justify-center mx-auto mb-4">

            {uploading ? (
              <Loader2 className="w-8 h-8 text-[#2563EB] animate-spin" />
            ) : (
              <Upload className="w-8 h-8 text-[#2563EB]" />
            )}

          </div>

          <p className="text-[#0F172A] mb-2 font-medium font-heading">

            {uploading
              ? 'Uploading Image...'
              : 'Upload Chladni Pattern'}

          </p>

          <p className="text-sm text-gray-500 mb-4">
            PNG, JPG, JPEG, WEBP — Maximum 10 MB
          </p>

          {/* Browse Button */}
          <button
            type="button"
            disabled={uploading}
            onClick={(e) => {
              e.stopPropagation()
              fileInputRef.current?.click()
            }}
            className="btn-primary text-sm py-2 px-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploading
              ? 'Uploading...'
              : 'Browse Image'}
          </button>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/jpg,image/webp,image/*"
            onChange={handleFileSelect}
            className="hidden"
          />

        </div>

      ) : (

        /* Uploaded Image */
        <div className="space-y-4">

          <div className="relative rounded-xl overflow-hidden bg-gray-100">

            <img
              src={imageUrl}
              alt="Uploaded Chladni pattern"
              className="w-full h-48 object-cover"
              onError={() => {
                setError(
                  'Image uploaded but preview could not be loaded.'
                )
              }}
            />

            {/* Gradient */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent pointer-events-none" />

            {/* Remove Button */}
            <button
              type="button"
              onClick={handleRemove}
              className="absolute top-3 right-3 p-2 bg-red-600/80 backdrop-blur-sm rounded-full hover:bg-red-600 transition-colors"
              title="Remove image"
            >

              <X className="w-4 h-4 text-white" />

            </button>

          </div>

          {/* File Information */}
          <div className="glass-card p-4 space-y-3">

            <p className="text-sm text-gray-700 font-medium break-all">
              {data.original_filename || data.filename}
            </p>

            <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">

              {data.file_size && (
                <div>
                  Size: {(data.file_size / 1024).toFixed(1)} KB
                </div>
              )}

              {data.width && data.height && (
                <div>
                  {data.width} × {data.height}
                </div>
              )}

            </div>

            {/* Success */}
            <div className="flex items-center gap-2 text-green-600 text-sm font-medium">

              <CheckCircle className="w-4 h-4" />

              <span>
                Image uploaded successfully
              </span>

            </div>

          </div>

        </div>

      )}

    </div>
  )
}

export default ImageUploader
```
