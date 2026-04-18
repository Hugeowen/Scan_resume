import os
from openai import OpenAI
import json
import re

api_key = os.getenv('ARK_API_KEY') or "ark-9195b9cf-64ec-4544-ac7e-2a40f729a6a1-88e47"

client = OpenAI(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key,
)

def extract_job_requirements(job_description):
    """使用AI提取岗位需求关键词和要求"""
    prompt = f"""
    你是一个专业的招聘分析师。请从以下岗位描述中提取关键信息，并严格以JSON格式返回：
    {{
        "position": "岗位名称",
        "requiredSkills": ["必需技能1", "必需技能2", ...],
        "preferredSkills": ["优先技能1", "优先技能2", ...],
        "minWorkYears": "最低工作年限要求（数字或空字符串）",
        "educationRequirement": "学历要求",
        "keyResponsibilities": ["主要职责1", "主要职责2", ...],
        "certificates": ["需要的证书1", "需要的证书2", ...]
    }}
    
    岗位描述：
    {job_description}
    """
    
    try:
        response = client.chat.completions.create(
            model="doubao-seed-1-8-251228",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        print(f"岗位需求提取失败: {e}")
        return {
            "position": "",
            "requiredSkills": [],
            "preferredSkills": [],
            "minWorkYears": "",
            "educationRequirement": "",
            "keyResponsibilities": [],
            "certificates": []
        }

def calculate_match_score(resume_info, job_requirements):
    """计算简历与岗位的匹配度评分"""
    try:
        prompt = f"""
        你是一个专业的HR匹配评估专家。请根据以下简历信息和岗位需求，计算匹配度评分。
        
        简历信息：
        {json.dumps(resume_info, ensure_ascii=False)}
        
        岗位需求：
        {json.dumps(job_requirements, ensure_ascii=False)}
        
        请严格以JSON格式返回评分结果：
        {{
            "overallScore": "总体匹配分数(0-100)",
            "skillScore": "技能匹配分数(0-100)",
            "experienceScore": "经验匹配分数(0-100)",
            "educationScore": "学历匹配分数(0-100)",
            "matchedSkills": ["已匹配的技能1", "已匹配的技能2", ...],
            "missingSkills": ["缺失的必需技能1", "缺失的必需技能2", ...],
            "analysis": "详细的匹配分析说明"
        }}
        """
        
        response = client.chat.completions.create(
            model="doubao-seed-1-8-251228",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        print(f"匹配评分失败: {e}")
        return {
            "overallScore": "0",
            "skillScore": "0",
            "experienceScore": "0",
            "educationScore": "0",
            "matchedSkills": [],
            "missingSkills": [],
            "analysis": f"评分失败: {str(e)}"
        }

def extract_info(resume_text):
    """用豆包API从简历文本中提取4个核心字段"""
    prompt = f"""
    你是一个简历解析助手。请从以下简历文本中提取信息，并严格以JSON格式返回，不要包含其他文字：
    {{
        "name": "姓名（如果没有则返回空字符串）",
        "phone": "电话（如果没有则返回空字符串）",
        "email": "邮箱（如果没有则返回空字符串）",
        "address": "地址（如果没有则返回空字符串）"
        "intention": "求职意向（如果没有则返回空字符串）",
        "salary": "期望薪资（如果没有则返回空字符串）",
        "education": "学历背景（如果没有则返回空字符串）",
        "workExperience": "工作经历（如果没有则返回空字符串）",
        "project": "项目经历（如果没有则返回空字符串）",
        "workYear": "工作年限（如果没有则返回空字符串）",
        "skills": "技能（如果没有则返回空字符串）",
        "language": "语言（如果没有则返回空字符串）",
        "certificates": "证书（如果没有则返回空字符串）"
    }}
    
    简历文本：
    {resume_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="doubao-seed-1-8-251228",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        print(f"AI提取失败: {e}")
        # 失败时返回空的字段
        return {"name": "", "phone": "", "email": "", "address": "", "intention": "", "salary": "", "education": "", "workExperience": "", "project": "", "workYear": "", "skills": "", "language": "", "certificates": ""}
