import requests
import wikipedia
import arxiv
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any
import logging

class RetrievalSystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def search_wikipedia(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search Wikipedia for relevant information"""
        try:
            search_results = wikipedia.search(query, results=num_results)
            articles = []
            
            for title in search_results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    articles.append({
                        'title': page.title,
                        'summary': page.summary,
                        'url': page.url,
                        'content': page.content[:1000] + "..." if len(page.content) > 1000 else page.content
                    })
                except Exception as e:
                    self.logger.warning(f"Error retrieving Wikipedia page {title}: {e}")
                    continue
                    
            return articles
        except Exception as e:
            self.logger.error(f"Error in Wikipedia search: {e}")
            return []
    
    def search_arxiv(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search arXiv for academic papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=num_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in search:
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'url': result.entry_id,
                    'published': result.published.isoformat() if result.published else None,
                    'primary_category': result.primary_category,
                    'categories': result.categories
                })
            
            return papers
        except Exception as e:
            self.logger.error(f"Error in arXiv search: {e}")
            return []
    
    def scrape_web(self, url: str) -> Dict[str, Any]:
        """Scrape content from a web page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for phrase in lines if phrase.strip())
            full_text = ' '.join(chunks)
            
            return {
                'title': soup.title.string if soup.title else 'No Title',
                'content': full_text[:2000] + "..." if len(full_text) > 2000 else full_text,
                'url': url
            }
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return {}
    
    def search_general(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """General search combining multiple sources"""
        results = []
        
        # Search Wikipedia
        wiki_results = self.search_wikipedia(query, num_results // 2)
        results.extend(wiki_results)
        
        # Search arXiv (if applicable)
        if "research" in query.lower() or "paper" in query.lower():
            arxiv_results = self.search_arxiv(query, num_results // 3)
            results.extend(arxiv_results)
        
        return results