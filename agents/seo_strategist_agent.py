from .base_agent import BaseAgent
from models.schemas import MarketResearchResult, SEOStrategy
from typing import List, Dict

class SEOStrategistAgent(BaseAgent):
    def __init__(self):
        super().__init__("SEOStrategist")
    
    async def execute(self, research_result: MarketResearchResult) -> SEOStrategy:
        primary_keywords = await self._select_primary_keywords(research_result)
        long_tail_keywords = await self._generate_long_tail_keywords(primary_keywords)
        titles = await self._suggest_titles(primary_keywords, long_tail_keywords)
        meta_descriptions = await self._generate_meta_descriptions(titles)
        internal_links = await self._suggest_internal_links(primary_keywords)
        
        return SEOStrategy(
            primary_keywords=primary_keywords,
            long_tail_keywords=long_tail_keywords,
            suggested_titles=titles,
            meta_descriptions=meta_descriptions,
            internal_links=internal_links
        )
    
    async def _select_primary_keywords(self, research: MarketResearchResult) -> List[str]:
        # Select top keywords based on volume and difficulty
        sorted_keywords = sorted(
            research.trending_keywords,
            key=lambda x: research.search_volume_data.get(x, 0),
            reverse=True
        )
        return sorted_keywords[:5]
    
    async def _generate_long_tail_keywords(self, primary_keywords: List[str]) -> List[str]:
        system_prompt = """Generate long-tail keyword variations that are specific 
        and have commercial intent. Focus on question-based and location-based variations."""
        
        user_prompt = f"""
        Primary Keywords: {', '.join(primary_keywords)}
        
        Generate 8 long-tail keyword variations (3-5 words each).
        Return as comma-separated list.
        """
        
        result = await self._call_llm(system_prompt, user_prompt)
        return [kw.strip() for kw in result.split(',')]
    
    async def _suggest_titles(self, primary_kw: List[str], long_tail_kw: List[str]) -> List[str]:
        system_prompt = """Create compelling, SEO-optimized article titles that include 
        target keywords naturally. Make them click-worthy but not clickbait."""
        
        all_keywords = primary_kw + long_tail_kw
        user_prompt = f"""
        Keywords to target: {', '.join(all_keywords[:8])}
        
        Generate 5 article titles that incorporate these keywords naturally.
        Make them engaging and SEO-friendly.
        Return as numbered list.
        """
        
        result = await self._call_llm(system_prompt, user_prompt)
        return [title.strip().split('. ', 1)[-1] for title in result.split('\n') if title.strip()]
    
    async def _generate_meta_descriptions(self, titles: List[str]) -> List[str]:
        system_prompt = """Write compelling meta descriptions (150-160 characters) 
        that encourage clicks while accurately describing the content."""
        
        meta_descriptions = []
        for title in titles:
            user_prompt = f"Write a meta description for this article title: {title}"
            result = await self._call_llm(system_prompt, user_prompt)
            meta_descriptions.append(result.strip())
        
        return meta_descriptions
    
    async def _suggest_internal_links(self, keywords: List[str]) -> List[str]:
        # Generate internal link anchor text suggestions
        return [f"Learn more about {kw}" for kw in keywords[:3]]