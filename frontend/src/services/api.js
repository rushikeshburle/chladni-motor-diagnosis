import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Upload endpoints
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await axios.post(`${API_BASE_URL}/upload/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

export const uploadVideo = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await axios.post(`${API_BASE_URL}/upload/video`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

export const deleteFile = async (filename) => {
  const response = await axios.delete(`${API_BASE_URL}/upload/${filename}`)
  return response.data
}

// Diagnosis endpoints
export const analyzeDiagnosis = async (data) => {
  const response = await apiClient.post('/diagnosis/analyze', data)
  return response.data
}

// History endpoints
export const getHistory = async (params = {}) => {
  const response = await apiClient.get('/history/', { params })
  return response.data
}

export const getRecord = async (recordId) => {
  const response = await apiClient.get(`/history/${recordId}`)
  return response.data
}

export const deleteRecord = async (recordId) => {
  const response = await apiClient.delete(`/history/${recordId}`)
  return response.data
}

export const getStatistics = async () => {
  const response = await apiClient.get('/history/stats/summary')
  return response.data
}

export default apiClient
