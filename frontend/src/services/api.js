```javascript
import axios from 'axios'

// Render / Vercel API URL
const API_BASE_URL = `${import.meta.env.VITE_API_URL}/api`

// Axios client
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000,
})

// ===============================
// Upload Image
// ===============================
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

// ===============================
// Upload Video
// ===============================
export const uploadVideo = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/upload/video', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

// ===============================
// Delete Uploaded File
// ===============================
export const deleteFile = async (filename) => {
  const response = await apiClient.delete(`/upload/${filename}`)
  return response.data
}

// ===============================
// Diagnosis
// ===============================
export const analyzeDiagnosis = async (data) => {
  const response = await apiClient.post(
    '/diagnosis/analyze',
    data
  )

  return response.data
}

// ===============================
// History
// ===============================
export const getHistory = async (params = {}) => {
  const response = await apiClient.get('/history/', {
    params,
  })

  return response.data
}

// ===============================
// Get Single History Record
// ===============================
export const getRecord = async (recordId) => {
  const response = await apiClient.get(
    `/history/${recordId}`
  )

  return response.data
}

// ===============================
// Delete History Record
// ===============================
export const deleteRecord = async (recordId) => {
  const response = await apiClient.delete(
    `/history/${recordId}`
  )

  return response.data
}

// ===============================
// Statistics
// ===============================
export const getStatistics = async () => {
  const response = await apiClient.get(
    '/history/stats/summary'
  )

  return response.data
}

// Export Axios Client
export default apiClient
```
