import type { UploadResponse, JobAnalysisResponse, MatchResponse, ResumeInfo } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const uploadResume = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable && onProgress) {
        const progress = Math.round((event.loaded / event.total) * 100)
        onProgress(progress)
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        resolve(JSON.parse(xhr.responseText))
      } else {
        reject(new Error('Upload failed'))
      }
    })

    xhr.addEventListener('error', () => {
      reject(new Error('Upload failed'))
    })

    xhr.open('POST', `${API_BASE_URL}/upload`)
    xhr.send(formData)
  })
}

// 分析岗位需求
export const analyzeJob = async (jobDescription: string): Promise<JobAnalysisResponse> => {
  const response = await fetch(`${API_BASE_URL}/analyze-job`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ jobDescription })
  })

  if (!response.ok) {
    throw new Error('Job analysis failed')
  }

  return response.json()
}

// 简历与岗位匹配
export const matchResume = async (resumeData: ResumeInfo, jobDescription: string): Promise<MatchResponse> => {
  const response = await fetch(`${API_BASE_URL}/match`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ resumeData, jobDescription })
  })

  if (!response.ok) {
    throw new Error('Match failed')
  }

  return response.json()
}


