import ollama
import requests
from typing import List, Dict, Any
import logging

class AIAssistant:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
    
    def summarize_content(self, content: str, max_length: int = 300) -> str:
        """Summarize content using local or cloud model"""
        try:
            prompt = f"Summarize the following content in {max_length} words or less:\n\n{content}"
            
            # Try using Ollama first (local model)
            try:
                response = ollama.generate(model=self.model_name, prompt=prompt)
                return response['response']
            except Exception as e:
                self.logger.warning(f"Ollama not available, falling back to basic summarization")
                # Fallback to simple truncation for demonstration
                return content[:max_length] + "..." if len(content) > max_length else content
                
        except Exception as e:
            self.logger.error(f"Error in summarization: {e}")
            return "Error generating summary"
    
    def rank_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rank search results based on relevance to query"""
        try:
            # Simple ranking based on keyword matching
            ranked_results = []
            
            for result in results:
                score = 0
                
                # Score based on query terms in title
                if 'title' in result:
                    for term in query.lower().split():
                        if term in result['title'].lower():
                            score += 1
                
                # Score based on query terms in summary/content
                content = result.get('summary', '') + result.get('content', '')
                for term in query.lower().split():
                    if term in content.lower():
                        score += 1
                
                result['relevance_score'] = score
                ranked_results.append(result)
            
            # Sort by relevance score (descending)
            ranked_results.sort(key=lambda x: x['relevance_score'], reverse=True)
            return ranked_results
            
        except Exception as e:
            self.logger.error(f"Error in ranking results: {e}")
            return results