from .base_agent import BaseAgent
from models.schemas import BlogArticle, QualityReport
from typing import List, Dict, Optional, Any


class QualityReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__("QualityReviewer")
    
    async def execute(self, article: BlogArticle) -> QualityReport:
        grammar_score = await self._check_grammar(article.content)
        readability_score = article.readability_score
        keyword_density = self._calculate_keyword_density(article.content, article.keywords)
        plagiarism_risk = await self._check_plagiarism_risk(article.content)
        suggestions = await self._generate_suggestions(article)
        
        return QualityReport(
            grammar_score=grammar_score,
            readability_score=readability_score,
            keyword_density=keyword_density,
            plagiarism_risk=plagiarism_risk,
            suggestions=suggestions
        )
    
    async def _check_grammar(self, content: str) -> float:
        # Simplified grammar check using LLM
        system_prompt = """Analyze the text for grammar, spelling, and style issues. 
        Rate the overall quality from 0-100."""
        
        user_prompt = f"Analyze this content for grammar quality:\n\n{content[:1000]}..."
        
        result = await self._call_llm(system_prompt, user_prompt)
        
        # Extract score from response (simplified)
        try:
            score = float([word for word in result.split() if word.replace('.', '').isdigit()][-1])
            return min(max(score, 0), 100)
        except:
            return 85.0  # Default score
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        content_lower = content.lower()
        total_words = len(content.split())
        
        density = {}
        for keyword in keywords:
            count = content_lower.count(keyword.lower())
            density[keyword] = (count / total_words) * 100
        
        return density
    
    async def _check_plagiarism_risk(self, content: str) -> str:
        # Simplified plagiarism check
        system_prompt = """Assess if this content appears to be original or potentially 
        plagiarized. Return: 'Low', 'Medium', or 'High' risk."""
        
        user_prompt = f"Assess plagiarism risk for:\n\n{content[:500]}..."
        
        result = await self._call_llm(system_prompt, user_prompt)
        
        risk_levels = ['Low', 'Medium', 'High']
        for level in risk_levels:
            if level.lower() in result.lower():
                return level
        
        return 'Low'
    
    async def _generate_suggestions(self, article: BlogArticle) -> List[str]:
        suggestions = []
        
        # Check readability
        if article.readability_score < 60:
            suggestions.append("Consider simplifying sentences for better readability")
        
        # Check keyword density
        for keyword, density in self._calculate_keyword_density(article.content, article.keywords).items():
            if density > 3:
                suggestions.append(f"Reduce keyword density for '{keyword}' - currently {density:.1f}%")
        
        # Check length
        if article.word_count < 1000:
            suggestions.append("Consider expanding content for better SEO performance")
        
        return suggestions