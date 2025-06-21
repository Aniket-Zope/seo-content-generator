from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class BusinessInput(BaseModel):
    business_type: str
    product_service: str
    target_audience: str
    niche_keywords: List[str]
    content_tone: Optional[str] = "professional"
    preferred_length: Optional[int] = 1500

class MarketResearchResult(BaseModel):
    trending_keywords: List[str]
    competitor_insights: List[Dict[str, str]]
    search_volume_data: Dict[str, int]
    difficulty_scores: Dict[str, float]

class ArticleRequest(BaseModel):
    title: str
    keywords: List[str]
    content_type: str = "blog_post"


class SEOStrategy(BaseModel):
    primary_keywords: List[str]
    long_tail_keywords: List[str]
    suggested_titles: List[str]
    meta_descriptions: List[str]
    internal_links: List[str]

class ContentPlan(BaseModel):
    calendar_days: int
    content_schedule: List[Dict[str, str]]
    keyword_mapping: Dict[str, List[str]]
    content_types: List[str]

class BlogArticle(BaseModel):
    title: str
    meta_description: str
    content: str
    keywords: List[str]
    word_count: int
    readability_score: float
    seo_score: float

class QualityReport(BaseModel):
    grammar_score: float
    readability_score: float
    keyword_density: Dict[str, float]
    plagiarism_risk: str
    suggestions: List[str]

class PerformanceEstimate(BaseModel):
    estimated_ranking: int
    traffic_potential: int
    competition_level: str
    success_probability: float

# ✅ Response Models
class ArticleResponse(BaseModel):
    article: BlogArticle
    quality_report: QualityReport
    performance_estimate: PerformanceEstimate

class APIResponse(BaseModel):
    success: bool
    data: ArticleResponse