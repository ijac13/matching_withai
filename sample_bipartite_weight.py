import networkx as nx
from networkx.algorithms import bipartite

# Initialise the graph
B = nx.Graph()
# Add nodes with the node attribute "bipartite"
top_nodes = [1, 2]
bottom_nodes = ["A", "B", "C", "D"]
B.add_nodes_from(top_nodes, bipartite=0)
B.add_nodes_from(bottom_nodes, bipartite=1)
# Add edges with weights
B.add_edge(1, "A", weight = 1)
B.add_edge(1, "B", weight = 4)
B.add_edge(1, "C", weight = 2)
B.add_edge(1, "D", weight = 1)
B.add_edge(2, "A", weight = 3)
B.add_edge(2, "B", weight = 1)
B.add_edge(2, "C", weight = 2)
B.add_edge(2, "D", weight = 2)
print("B:",B)
#Obtain the minimum weight full matching
my_matching = bipartite.matching.minimum_weight_full_matching(B, top_nodes, "weight")

print("my_matching:", my_matching)
#my_matching: {1: 'D', 2: 'B', 'D': 1, 'B': 2}
#even same weight can work