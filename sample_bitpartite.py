import networkx as nx

# Create a new graph
G = nx.Graph()

# Add mentors and mentees as nodes
mentors = ['Mentor1', 'Mentor2', 'Mentor3']
mentees = ['Mentee1', 'Mentee2', 'Mentee3']
G.add_nodes_from(mentors, bipartite=0)  # Label mentors as one set
G.add_nodes_from(mentees, bipartite=1)  # Label mentees as the other set

# Add edges based on your matching criteria
G.add_edges_from([('Mentor1', 'Mentee2'), ('Mentor1', 'Mentee3')])
G.add_edges_from([('Mentor2', 'Mentee1'), ('Mentor3', 'Mentee3')])

# Try to define the two sets based on a known starting node
try:
    top_nodes, bottom_nodes = nx.bipartite.sets(G, top_nodes={'Mentor1'})
except nx.AmbiguousSolution as e:
    print("Error:", e)
    # Handle the error or provide a fallback mechanism

# Find the maximum matching
max_matching = nx.bipartite.maximum_matching(G, top_nodes)

print("max_matching:", max_matching)
