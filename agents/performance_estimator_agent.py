from .base_agent import BaseAgent
from models.schemas import BlogArticle, QualityReport, PerformanceEstimate
from typing import List, Dict

class PerformanceEstimatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("PerformanceEstimator")
    
    async def execute(self, article: BlogArticle, quality_report: QualityReport) -> PerformanceEstimate:
        ranking_estimate = await self._estimate_ranking(article, quality_report)
        traffic_potential = await self._estimate_traffic(article)
        competition_level = await self._assess_competition(article.keywords)
        success_probability = self._calculate_success_probability(
            article, quality_report, ranking_estimate
        )
        
        return PerformanceEstimate(
            estimated_ranking=ranking_estimate,
            traffic_potential=traffic_potential,
            competition_level=competition_level,
            success_probability=success_probability
        )
    
    async def _estimate_ranking(self, article: BlogArticle, quality_report: QualityReport) -> int:
        # Simplified ranking estimation based on content quality
        base_score = (
            article.seo_score * 0.4 +
            quality_report.grammar_score * 0.2 +
            quality_report.readability_score * 0.2 +
            (100 - sum(quality_report.keyword_density.values())) * 0.2
        )
        
        # Convert to ranking estimate (1-50)
        if base_score >= 90:
            return 1
        elif base_score >= 80:
            return 3
        elif base_score >= 70:
            return 7
        elif base_score >= 60:
            return 15
        else:
            return 25
    
    async def _estimate_traffic(self, article: BlogArticle) -> int:
        # Simplified traffic estimation
        base_traffic = article.word_count * 2  # Base calculation
        
        # Adjust for SEO score
        multiplier = article.seo_score / 100
        
        return int(base_traffic * multiplier)
    
    async def _assess_competition(self, keywords: List[str]) -> str:
        # Simplified competition assessment
        system_prompt = """Assess the competition level for these keywords in SEO. 
        Return: 'Low', 'Medium', or 'High'."""
        
        user_prompt = f"Keywords: {', '.join(keywords)}"
        
        result = await self._call_llm(system_prompt, user_prompt)
        
        levels = ['Low', 'Medium', 'High']
        for level in levels:
            if level.lower() in result.lower():
                return level
        
        return 'Medium'
    
    def _calculate_success_probability(self, article: BlogArticle, 
                                     quality_report: QualityReport, 
                                     ranking: int) -> float:
        # Calculate success probability based on various factors
        quality_score = (
            article.seo_score +
            quality_report.grammar_score +
            quality_report.readability_score
        ) / 3
        
        ranking_factor = max(0, (51 - ranking) / 50)  # Higher rank = higher probability
        
        return min((quality_score / 100) * ranking_factor * 100, 95.0)
