from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pdf_parser import parse_pdf
from ai_extractor import extract_info, extract_job_requirements, calculate_match_score

# 请求模型
class JobDescriptionRequest(BaseModel):
    jobDescription: str

class MatchRequest(BaseModel):
    resumeData: dict
    jobDescription: str

app = FastAPI(title="AI简历信息提取系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 临时文件夹
os.makedirs("temp", exist_ok=True)

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """上传PDF简历，直接返回姓名、电话、邮箱、地址"""
    try:
        # 1. 保存上传的PDF文件
        file_path = f"temp/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. 解析PDF文本
        resume_text = parse_pdf(file_path)
        
        # 3. 用AI提取4个核心字段
        resume_info = extract_info(resume_text)
        
        # 4. 删除临时文件
        os.remove(file_path)
        
        # 5. 直接返回结果（只包含4个字段）
        return JSONResponse(content={
            "code": 200,
            "message": "提取成功",
            "data": {
                "name": resume_info.get("name", ""),
                "phone": resume_info.get("phone", ""),
                "email": resume_info.get("email", ""),
                "address": resume_info.get("address", ""),
                "intention": resume_info.get("intention", ""),
                "salary": resume_info.get("salary", ""),
                "education": resume_info.get("education", ""),
                "workExperience": resume_info.get("workExperience", ""),
                "project": resume_info.get("project", ""),
                "workYear": resume_info.get("workYear", ""),
                "skills": resume_info.get("skills", ""),
                "language": resume_info.get("language", ""),
                "certificates": resume_info.get("certificates", "")
            }
        })
    except Exception as e:
        return JSONResponse(content={
            "code": 500,
            "message": f"提取失败: {str(e)}",
            "data": {
                "name": "", "phone": "", "email": "", "address": "",
                "intention": "", "salary": "", "education": "", "workExperience": "",
                "project": "", "workYear": "", "skills": "", "language": "", "certificates": ""
            }
        }, status_code=500)

@app.post("/analyze-job")
async def analyze_job(request: JobDescriptionRequest):
    """分析岗位需求，提取关键词和要求"""
    try:
        job_requirements = extract_job_requirements(request.jobDescription)
        return JSONResponse(content={
            "code": 200,
            "message": "分析成功",
            "data": job_requirements
        })
    except Exception as e:
        return JSONResponse(content={
            "code": 500,
            "message": f"分析失败: {str(e)}",
            "data": None
        }, status_code=500)

@app.post("/match")
async def match_resume_job(request: MatchRequest):
    """将简历与岗位需求进行匹配评分"""
    try:
        # 1. 提取岗位需求
        job_requirements = extract_job_requirements(request.jobDescription)
        
        # 2. 计算匹配度
        match_result = calculate_match_score(request.resumeData, job_requirements)
        
        return JSONResponse(content={
            "code": 200,
            "message": "匹配成功",
            "data": {
                "jobRequirements": job_requirements,
                "matchResult": match_result
            }
        })
    except Exception as e:
        return JSONResponse(content={
            "code": 500,
            "message": f"匹配失败: {str(e)}",
            "data": None
        }, status_code=500)

# 本地测试入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)