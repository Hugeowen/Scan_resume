import PyPDF2
import re

def parse_pdf(file_path):
    """解析PDF文件，提取并清洗文本"""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    
    # 简单清洗：去除多余空格和换行
    text = re.sub(r"\s+", " ", text).strip()
    return text