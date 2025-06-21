from fastapi import FastAPI, HTTPException, Body
from models.schemas import ArticleRequest, APIResponse
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import *
from workflow.seo_workflow import SEOWorkflow
import uvicorn

app = FastAPI(
    title="SEO Content Generator API",
    description="AI-powered SEO content generation and planning system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow
seo_workflow = SEOWorkflow()

@app.get("/")
async def root():
    return {"message": "SEO Content Generator API is running!"}

@app.post("/generate-plan", response_model=dict)
async def generate_plan(business_input: BusinessInput = Body(...)):
    """Generate complete SEO content plan"""
    try:
        result = await seo_workflow.generate_complete_plan(business_input)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-article", response_model=APIResponse)
async def generate_article(request: ArticleRequest = Body(...)):
    try:
        result = await seo_workflow.generate_article(
            request.title,
            request.keywords,
            request.content_type
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/evaluate-content", response_model=dict)
async def evaluate_content(article: BlogArticle = Body(...)):
    """Evaluate existing content quality"""
    try:
        quality_report = await seo_workflow.quality_reviewer_agent.execute(article)
        performance_estimate = await seo_workflow.performance_estimator_agent.execute(
            article, quality_report
        )
        return {
            "success": True,
            "data": {
                "quality_report": quality_report.dict(),
                "performance_estimate": performance_estimate.dict()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}



if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

