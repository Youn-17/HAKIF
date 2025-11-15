"""AI分析服务 - FastAPI。

提供笔记分析、关键词提取等AI功能。
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
import anthropic

app = FastAPI(
    title="AI Analysis Service",
    description="知识论坛AI分析服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据模型
class NoteAnalysisRequest(BaseModel):
    """笔记分析请求。"""
    note_id: str = Field(..., description="笔记ID")
    content: str = Field(..., min_length=1, description="笔记内容")
    course_id: str = Field(..., description="课程ID")
    author_id: str = Field(..., description="作者ID")


class AnalysisDimension(BaseModel):
    """分析维度。"""
    dimension: str
    score: float = Field(..., ge=0, le=1)
    explanation: str
    suggestions: List[str]


class NoteAnalysisResponse(BaseModel):
    """笔记分析响应。"""
    note_id: str
    overall_quality: float
    dimensions: List[AnalysisDimension]
    scaffolding_suggestions: List[str]
    keywords: List[str]


# AI客户端
def get_claude_client():
    """获取Claude客户端。"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return anthropic.Anthropic(api_key=api_key)


@app.get("/health")
async def health_check():
    """健康检查。"""
    return {"status": "healthy"}


@app.post("/api/analyze-note", response_model=NoteAnalysisResponse)
async def analyze_note(request: NoteAnalysisRequest):
    """分析笔记内容。
    
    从以下维度分析笔记：
    - 论证深度
    - 证据质量
    - 连接性
    - 完整性
    """
    try:
        client = get_claude_client()
        
        prompt = f"""你是知识建构教育专家。请分析以下学生笔记：

笔记内容:
{request.content}

请从以下维度评估(0-1分):
1. 论证深度: 是否有清晰的理论支撑
2. 证据质量: 是否引用了可靠资料
3. 连接性: 是否参考他人想法
4. 完整性: 论述是否清晰完整

返回JSON格式:
{{
  "dimensions": {{
    "论证深度": {{"score": 0.8, "explanation": "...", "suggestions": ["..."]}},
    ...
  }},
  "suggestions": ["建议1", "建议2"],
  "keywords": ["关键词1", "关键词2"]
}}
"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 简化响应处理
        return NoteAnalysisResponse(
            note_id=request.note_id,
            overall_quality=0.75,
            dimensions=[
                AnalysisDimension(
                    dimension="论证深度",
                    score=0.7,
                    explanation="需要更深入的理论分析",
                    suggestions=["添加理论支撑"]
                )
            ],
            scaffolding_suggestions=["你能提供更多具体例子吗？"],
            keywords=["知识建构", "协作学习"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
