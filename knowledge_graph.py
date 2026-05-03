import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import logging

class KnowledgeGraph:
    def __init__(self, db_path: str = "aurora_memory.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.graph = nx.DiGraph()
        self.load_graph()
    
    def load_graph(self):
        """Load the knowledge graph from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Load nodes (topics)
            cursor.execute('SELECT id, title FROM topics')
            topics = cursor.fetchall()
            
            for topic_id, title in topics:
                self.graph.add_node(topic_id, title=title)
            
            # Load edges (relationships)
            cursor.execute('''
                SELECT r.source_topic_id, r.target_topic_id, r.relationship_type
                FROM relationships r
            ''')
            
            relationships = cursor.fetchall()
            
            for source_id, target_id, rel_type in relationships:
                self.graph.add_edge(source_id, target_id, relationship=rel_type)
            
            conn.close()
        except Exception as e:
            self.logger.error(f"Error loading graph: {e}")
    
    def add_node(self, topic_id: int, title: str):
        """Add a node to the graph"""
        self.graph.add_node(topic_id, title=title)
    
    def add_edge(self, source_id: int, target_id: int, relationship_type: str):
        """Add an edge to the graph"""
        self.graph.add_edge(source_id, target_id, relationship=relationship_type)
    
    def get_related_topics(self, topic_id: int, depth: int = 2) -> List[Dict[str, Any]]:
        """Get topics related to a given topic within specified depth"""
        try:
            # Use BFS to find related topics
            related = []
            visited = {topic_id}
            queue = [(topic_id, 0)]  # (node_id, depth)
            seen_related = set()

            while queue:
                current_id, current_depth = queue.pop(0)

                if current_depth >= depth:
                    continue

                # Get neighbors
                neighbors = list(self.graph.neighbors(current_id))
                for neighbor_id in neighbors:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        if neighbor_id not in seen_related:
                            seen_related.add(neighbor_id)
                            related.append({
                                'id': neighbor_id,
                                'title': self.graph.nodes[neighbor_id]['title'],
                                'relationship': self.graph.get_edge_data(current_id, neighbor_id)['relationship']
                            })
                        queue.append((neighbor_id, current_depth + 1))

            return related
        except Exception as e:
            self.logger.error(f"Error finding related topics: {e}")
            return []
    
    def visualize(self, filename: str = "knowledge_graph.png"):
        """Visualize the knowledge graph"""
        try:
            plt.figure(figsize=(12, 8))
            
            # Get positions for nodes
            pos = nx.spring_layout(self.graph, k=1, iterations=50)
            
            # Draw nodes
            nx.draw_networkx_nodes(self.graph, pos, node_size=700, alpha=0.9)
            
            # Draw edges
            nx.draw_networkx_edges(self.graph, pos, arrowstyle='->', arrowsize=20)
            
            # Draw labels
            labels = {node: self.graph.nodes[node]['title'] for node in self.graph.nodes()}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
            
            plt.title("Aurora Knowledge Graph")
            plt.axis('off')
            plt.tight_layout()
            
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
        except Exception as e:
            self.logger.error(f"Error visualizing graph: {e}")
            return None
    
    def get_graph_info(self) -> Dict[str, Any]:
        """Get information about the graph"""
        if self.graph.number_of_nodes() == 0:
            is_connected = False
        elif self.graph.is_directed():
            is_connected = nx.is_weakly_connected(self.graph)
        else:
            is_connected = nx.is_connected(self.graph)

        return {
            'nodes': len(self.graph.nodes()),
            'edges': len(self.graph.edges()),
            'is_directed': self.graph.is_directed(),
            'is_connected': is_connected
        }