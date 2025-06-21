import asyncio
from typing import Dict, Any
from models.schemas import *
from agents.market_research_agent import MarketResearchAgent
from agents.seo_strategist_agent import SEOStrategistAgent
from agents.content_planner_agent import ContentPlannerAgent
from agents.blog_writer_agent import BlogWriterAgent
from agents.quality_reviewer_agent import QualityReviewerAgent
from agents.performance_estimator_agent import PerformanceEstimatorAgent

class SEOWorkflow:
    def __init__(self):
        self.market_research_agent = MarketResearchAgent()
        self.seo_strategist_agent = SEOStrategistAgent()
        self.content_planner_agent = ContentPlannerAgent()
        self.blog_writer_agent = BlogWriterAgent()
        self.quality_reviewer_agent = QualityReviewerAgent()
        self.performance_estimator_agent = PerformanceEstimatorAgent()
    
    async def generate_complete_plan(self, business_input: BusinessInput) -> Dict[str, Any]:
        """Generate complete SEO content plan"""
        
        # Step 1: Market Research
        research_result = await self.market_research_agent.execute(business_input)
        
        # Step 2: SEO Strategy
        seo_strategy = await self.seo_strategist_agent.execute(research_result)
        
        # Step 3: Content Planning
        content_plan = await self.content_planner_agent.execute(seo_strategy, days=7)
        
        return {
            "research": research_result.dict(),
            "strategy": seo_strategy.dict(),
            "plan": content_plan.dict()
        }
    
    async def generate_article(self, title: str, keywords: List[str], 
                             content_type: str = "blog_post") -> Dict[str, Any]:
        """Generate a single article with quality review and performance estimate"""
        
        # Step 1: Write Article
        article = await self.blog_writer_agent.execute(title, keywords, content_type)
        
        # Step 2: Quality Review
        quality_report = await self.quality_reviewer_agent.execute(article)
        
        # Step 3: Performance Estimate
        performance_estimate = await self.performance_estimator_agent.execute(
            article, quality_report
        )
        
        return {
            "article": article.dict(),
            "quality_report": quality_report.dict(),
            "performance_estimate": performance_estimate.dict()
        }
    
    async def generate_calendar_articles(self, content_plan: ContentPlan) -> List[Dict[str, Any]]:
        """Generate articles for entire content calendar"""
        
        articles = []
        for scheduled_content in content_plan.content_schedule:
            title = scheduled_content["title"]
            keywords = scheduled_content["keywords"].split(", ")
            content_type = scheduled_content["content_type"]
            
            article_data = await self.generate_article(title, keywords, content_type)
            article_data["scheduled_date"] = scheduled_content["date"]
            articles.append(article_data)
        
        return articles
