import textstat
from typing import List
from .base_agent import BaseAgent
from models.schemas import BlogArticle

class BlogWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("BlogWriter")
    
    async def execute(self, title: str, keywords: List[str], 
                     content_type: str = "blog_post", 
                     target_length: int = 1500) -> BlogArticle:
        
        content = await self._write_article(title, keywords, content_type, target_length)
        meta_description = await self._generate_meta_description(title, content)
        word_count = len(content.split())
        readability_score = textstat.flesch_reading_ease(content)
        seo_score = await self._calculate_seo_score(content, keywords)
        
        return BlogArticle(
            title=title,
            meta_description=meta_description,
            content=content,
            keywords=keywords,
            word_count=word_count,
            readability_score=readability_score,
            seo_score=seo_score
        )
    
    async def _write_article(self, title: str, keywords: List[str], 
                           content_type: str, target_length: int) -> str:
        
        system_prompt = f"""You are an expert SEO content writer. Write a {content_type} 
        that is informative, engaging, and optimized for search engines. 
        
        Guidelines:
        - Target length: ~{target_length} words
        - Use keywords naturally (not stuffed)
        - Include H2 and H3 headings
        - Write in a conversational yet professional tone
        - Include actionable insights
        - Use short paragraphs for readability
        """
        
        user_prompt = f"""
        Title: {title}
        Target Keywords: {', '.join(keywords)}
        Content Type: {content_type}
        
        Write a comprehensive article following SEO best practices.
        Include:
        1. Engaging introduction
        2. Well-structured body with subheadings
        3. Practical examples or tips
        4. Strong conclusion with call-to-action
        """
        
        return await self._call_llm(system_prompt, user_prompt)
    
    async def _generate_meta_description(self, title: str, content: str) -> str:
        system_prompt = """Write a compelling meta description (150-160 characters) 
        that summarizes the article and encourages clicks."""
        
        # Extract first few sentences for context
        content_preview = ' '.join(content.split()[:50])
        user_prompt = f"Title: {title}\nContent preview: {content_preview}\n\nWrite meta description:"
        
        return await self._call_llm(system_prompt, user_prompt)
    
    async def _calculate_seo_score(self, content: str, keywords: List[str]) -> float:
        # Simple SEO scoring based on keyword presence and density
        content_lower = content.lower()
        total_words = len(content.split())
        
        score = 0.0
        for keyword in keywords:
            keyword_count = content_lower.count(keyword.lower())
            density = keyword_count / total_words
            
            # Optimal density is 1-3%
            if 0.01 <= density <= 0.03:
                score += 20
            elif density > 0:
                score += 10
        
        # Bonus for headings, length, readability
        if '<h2>' in content.lower() or '##' in content:
            score += 10
        if total_words >= 1000:
            score += 10
        
        return min(score, 100.0)
