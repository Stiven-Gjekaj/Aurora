import argparse
import sys
from typing import List, Dict
from retrieval_system import RetrievalSystem
from memory_system import MemorySystem
from knowledge_graph import KnowledgeGraph
from ai_assistant import AIAssistant
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AuroraAssistant:
    def __init__(self):
        self.retrieval_system = RetrievalSystem()
        self.memory_system = MemorySystem()
        self.knowledge_graph = KnowledgeGraph()
        self.ai_assistant = AIAssistant()
        
    def research(self, query: str, num_results: int = 10) -> List[Dict]:
        """Perform research on a query"""
        logger.info(f"Researching: {query}")
        
        # Retrieve information
        results = self.retrieval_system.search_general(query, num_results)
        
        # Rank results
        ranked_results = self.ai_assistant.rank_results(results, query)
        
        # Summarize results
        summarized_results = []
        for result in ranked_results[:5]:  # Take top 5 for summarization
            summary = self.ai_assistant.summarize_content(
                result.get('content', result.get('summary', '')), 
                max_length=200
            )
            
            # Store in memory
            topic_id = self.memory_system.store_topic(
                title=result.get('title', 'Unknown'),
                summary=summary
            )
            
            # Store content
            self.memory_system.store_content(
                topic_id=topic_id,
                content_type='research',
                content=result.get('content', result.get('summary', ''))
            )
            
            summarized_results.append({
                'title': result.get('title', ''),
                'summary': summary,
                'url': result.get('url', ''),
                'relevance_score': result.get('relevance_score', 0)
            })
        
        return summarized_results
    
    def explore_knowledge_graph(self):
        """Explore the knowledge graph"""
        graph_info = self.knowledge_graph.get_graph_info()
        logger.info(f"Knowledge Graph Info: {graph_info}")
        
        # Get all topics
        topics = self.memory_system.get_all_topics()
        logger.info(f"Found {len(topics)} topics in memory")
        
        for topic in topics[:3]:  # Show first 3 topics
            relationships = self.memory_system.get_topic_relationships(topic['title'])
            logger.info(f"Topic: {topic['title']}")
            logger.info(f"  Relationships: {len(relationships)}")
            for rel in relationships[:2]:  # Show first 2 relationships
                logger.info(f"    -> {rel['relationship_type']} {rel['target_topic']}")
    
    def visualize_graph(self):
        """Visualize the knowledge graph"""
        filename = self.knowledge_graph.visualize("aurora_knowledge_graph.png")
        if filename:
            logger.info(f"Knowledge graph visualized as {filename}")
        else:
            logger.error("Failed to visualize knowledge graph")

def main():
    parser = argparse.ArgumentParser(description='Aurora - Personal AI Research Assistant')
    parser.add_argument('--query', help='Research query')
    parser.add_argument('--explore', action='store_true', help='Explore knowledge graph')
    parser.add_argument('--visualize', action='store_true', help='Visualize knowledge graph')
    
    args = parser.parse_args()
    
    assistant = AuroraAssistant()
    
    if args.query:
        results = assistant.research(args.query)
        print(f"\nResearch Results for '{args.query}':")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Summary: {result['summary']}")
            print(f"   Relevance: {result['relevance_score']}")
            print()
    
    if args.explore:
        assistant.explore_knowledge_graph()
    
    if args.visualize:
        assistant.visualize_graph()

if __name__ == "__main__":
    main()