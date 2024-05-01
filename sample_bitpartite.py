import networkx as nx

# Create a new graph
G = nx.Graph()

# Add mentors and mentees as nodes
mentors = ['Mentor1', 'Mentor2', 'Mentor3']
mentees = ['Mentee1', 'Mentee2', 'Mentee3']
G.add_nodes_from(mentors, bipartite=0)  # Label mentors as one set
G.add_nodes_from(mentees, bipartite=1)  # Label mentees as the other set

# Add edges based on your matching criteria
# For example, if Mentor1 is a good match for Mentee2 and Mentee3:
G.add_edges_from([('Mentor1', 'Mentee2'), ('Mentor1', 'Mentee3')])

# Ensure every node is part of at least one edge (i.e., every mentor and mentee has at least one potential match)
# For demonstration, let's add some dummy edges
G.add_edges_from([('Mentor2', 'Mentee1'), ('Mentor3', 'Mentee3')])

# Explicitly define the two sets to avoid ambiguity
top_nodes, bottom_nodes = nx.bipartite.sets(G)

# Find the maximum matching
max_matching = nx.bipartite.maximum_matching(G, top_nodes)

print(max_matching)
