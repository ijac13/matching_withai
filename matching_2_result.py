import pandas as pd
import networkx as nx

# Loading the DataFrames from CSV files
mentors_df = pd.read_csv('mentors_df.csv')
mentees_df = pd.read_csv('mentees_df.csv')
match_scores_df = pd.read_csv('match_1.5_score.csv')

# After loading the DataFrame, check the columns to ensure 'Match Score' is present
print("match_scores_df:", match_scores_df.columns)


# 1. Prepare the Score Lookup Dictionary
# Creating a lookup dictionary for match scores for faster access
score_lookup = {(row['Mentor'], row['Mentee']): row['Match Score'] for index, row in match_scores_df.iterrows()}

#debug
# Print a few entries from the dictionary to verify its structure
print(list(score_lookup.items())[:5])
print(mentors_df.index.duplicated().sum())  # Check for duplicate mentor emails
print("Total mentor opportunities (including duplicates):", len(mentors_df.index) * 3)
print("Total mentees available:", len(mentees_df.index))


# 2.Create a new bipartite graph
# 'Email' is the index for both mentors_df and mentees_df
# Adding mentor nodes - duplicating each mentor node 3 times to allow up to 3 matches
B = nx.Graph()

# Adding mentor nodes - duplicating each mentor node 3 times to allow up to 3 matches
for email in mentors_df.index:  # Correct use of index
    for i in range(1, 4):
        B.add_node(f"{email}_{i}", bipartite=0)

# Add mentee nodes using the index
B.add_nodes_from(mentees_df.index, bipartite=1)

# Add edges between mentors and mentees using negative weights for max weight matching
for (mentor, mentee), score in score_lookup.items():
    for i in range(1, 4):
        B.add_edge(f"{mentor}_{i}", mentee, weight=-score)


# Debug: Print total edges in the graph
print("Total edges in the graph:", B.number_of_edges())

# 3. Process the Maximum Matching using the corrected approach for top_nodes
top_nodes = {f"{email}_{i}" for email in mentors_df.index for i in range(1, 4)}  # Use index directly
matching = nx.algorithms.bipartite.maximum_matching(B, top_nodes=top_nodes)

# Filter to include only mentor to mentee matches and clean up the mentor identifiers
final_matching = {ment.split('_')[0]: mentee for ment, mentee in matching.items() if "_" in ment and B.nodes[ment]['bipartite'] == 0}

# Create match results including match scores
match_results = [{
    'Mentor': mentor,
    'Mentee': mentee,
    'Match Score': score_lookup.get((mentor, mentee), 0)
} for mentor, mentee in final_matching.items()]

# Convert match results to a DataFrame and sort
final_matches_df = pd.DataFrame(match_results)
final_matches_df = final_matches_df.sort_values(by=['Match Score', 'Mentor', 'Mentee'], ascending=[False, True, True])

# 4. Output
print('Exporting match_2.1_matches.csv')
print(final_matches_df.head())
final_matches_df.to_csv('match_2.1_matches.csv', index=False)

# Count unique mentors who got matched
unique_mentors_matched = final_matches_df['Mentor'].nunique()
unique_mentees_matched = final_matches_df['Mentee'].nunique()

print(f"Number of mentors who got matched: {unique_mentors_matched}")
print(f"Number of mentees who got matched: {unique_mentees_matched}")

