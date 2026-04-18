// Resume data types - 适配后端返回的完整数据结构
export interface ResumeInfo {
  name: string
  phone: string
  email: string
  address: string
  intention: string
  salary: string
  education: string
  workExperience: string
  project: string
  workYear: string
  skills: string
  language: string
  certificates: string
}

// 岗位需求分析结果
export interface JobRequirements {
  position: string
  requiredSkills: string[]
  preferredSkills: string[]
  minWorkYears: string
  educationRequirement: string
  keyResponsibilities: string[]
  certificates: string[]
}

// 匹配评分结果
export interface MatchResult {
  overallScore: string
  skillScore: string
  experienceScore: string
  educationScore: string
  matchedSkills: string[]
  missingSkills: string[]
  analysis: string
}

// 后端返回的响应结构
export interface UploadResponse {
  code: number
  message: string
  data: ResumeInfo
}

export interface JobAnalysisResponse {
  code: number
  message: string
  data: JobRequirements
}

export interface MatchResponse {
  code: number
  message: string
  data: {
    jobRequirements: JobRequirements
    matchResult: MatchResult
  }
}
