from datetime import datetime, timedelta
from typing import List, Dict
from .base_agent import BaseAgent
from models.schemas import SEOStrategy, ContentPlan

class ContentPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("ContentPlanner")
    
    async def execute(self, seo_strategy: SEOStrategy, days: int = 7) -> ContentPlan:
        content_schedule = await self._create_schedule(seo_strategy, days)
        keyword_mapping = await self._map_keywords_to_content(seo_strategy)
        content_types = await self._determine_content_types(seo_strategy)
        
        return ContentPlan(
            calendar_days=days,
            content_schedule=content_schedule,
            keyword_mapping=keyword_mapping,
            content_types=content_types
        )
    
    async def _create_schedule(self, strategy: SEOStrategy, days: int) -> List[Dict[str, str]]:
        schedule = []
        start_date = datetime.now()
        
        titles = strategy.suggested_titles
        for i in range(min(days, len(titles))):
            publish_date = start_date + timedelta(days=i)
            schedule.append({
                "date": publish_date.strftime("%Y-%m-%d"),
                "title": titles[i],
                "keywords": ", ".join(strategy.primary_keywords[:2]),
                "content_type": self._assign_content_type(i),
                "status": "planned"
            })
        
        return schedule
    
    def _assign_content_type(self, index: int) -> str:
        types = ["how-to", "listicle", "guide", "comparison", "tutorial"]
        return types[index % len(types)]
    
    async def _map_keywords_to_content(self, strategy: SEOStrategy) -> Dict[str, List[str]]:
        mapping = {}
        all_keywords = strategy.primary_keywords + strategy.long_tail_keywords
        
        for i, title in enumerate(strategy.suggested_titles):
            # Assign 2-3 keywords per article
            assigned_keywords = all_keywords[i*2:(i*2)+3]
            mapping[title] = assigned_keywords
        
        return mapping
    
    async def _determine_content_types(self, strategy: SEOStrategy) -> List[str]:
        return ["blog_post", "how_to_guide", "listicle", "product_review", "comparison"]