import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

#### one mentor match to one mentee
#### max matches = the number of

# Loading the DataFrames from CSV files
match_scores_df = pd.read_csv('match_1.5_score.csv')


# After loading the DataFrame, check the columns to ensure 'Match Score' is present
print("match_scores_df:", match_scores_df.columns)

unique_mentors = match_scores_df['Mentor'].unique()
unique_mentees = match_scores_df['Mentee'].unique()
# Verify counts
print("Number of unique mentors:", len(unique_mentors))
print("Number of unique mentees:", len(unique_mentees))

# debug - Check for any overlap
# overlap = set(unique_mentors) & set(unique_mentees)
# print("Overlap between mentors and mentees:", overlap)


# Add unique prefixes to mentors and mentees
mentors_prefixed = ['mentor_' + str(mentor) for mentor in match_scores_df['Mentor'].unique()]
mentees_prefixed = ['mentee_' + str(mentee) for mentee in match_scores_df['Mentee'].unique()]

# Reinitialize the graph
B = nx.Graph()

# Add prefixed nodes
B.add_nodes_from(mentors_prefixed, bipartite=0)
B.add_nodes_from(mentees_prefixed, bipartite=1)

# Add edges with prefixed node identifiers
for idx, row in match_scores_df.iterrows():
    mentor = 'mentor_' + str(row['Mentor'])
    mentee = 'mentee_' + str(row['Mentee'])
    match_score = row['Match Score']
    B.add_edge(mentor, mentee, weight=-match_score)
    
print("B nodes and edge:",B)
# After adding all edges
print("Total edges in the graph:", B.number_of_edges())

# Obtain the minimum weight full matching
matching = bipartite.matching.minimum_weight_full_matching(B, weight='weight')
# print("Matching:", matching)

# Correctly extract match scores and include them in the result
match_results = []
for mentor, mentee in matching.items():
    if mentor in B and mentee in B and B.nodes[mentor]['bipartite'] == 0:
        # Retrieve the original match score (invert the negative weight stored in the graph)
        match_score = -B[mentor][mentee]['weight']
        mentor_cleaned = mentor.replace('mentor_', '')  # Clean mentor prefix
        mentee_cleaned = mentee.replace('mentee_', '')  # Clean mentee prefix
        match_results.append({
            'Mentor': mentor_cleaned,
            'Mentee': mentee_cleaned,
            'Match Score': match_score
        })

# Convert match results to a DataFrame
final_matches_df = pd.DataFrame(match_results)

# Sort the DataFrame by 'Match Score' descending, then 'Mentor' and 'Mentee' ascending
final_matches_df = final_matches_df.sort_values(by=['Match Score', 'Mentor', 'Mentee'], ascending=[False, True, True])

# Output the results
print('Exporting match_2.1_matches.csv')
print(final_matches_df.head())
final_matches_df.to_csv('match_2.1_matches.csv', index=False)

# Count unique mentors and mentees who got matched
unique_mentors_matched = final_matches_df['Mentor'].nunique()
unique_mentees_matched = final_matches_df['Mentee'].nunique()

print(f"Number of mentors who got matched: {unique_mentors_matched}")
print(f"Number of mentees who got matched: {unique_mentees_matched}")


## rematch unmatched mentees
# Identify matched mentees from results
matched_mentees = set(final_matches_df['Mentee'])

# Find unmatched mentees
all_mentees = set(match_scores_df['Mentee'].unique())
unmatched_mentees = all_mentees - matched_mentees
unmatched_mentees_list = list(unmatched_mentees)  # Convert set to list
unmatched_mentees_df = pd.DataFrame(unmatched_mentees_list, columns=['Mentee'])  # Create DataFrame

# Reinitialize the graph
B2 = nx.Graph()
# Add unique prefixes to mentors and mentees
mentors_prefixed = ['mentor_' + str(mentor) for mentor in match_scores_df['Mentor'].unique()]
mentees_prefixed = ['mentee_' + str(mentee) for mentee in unmatched_mentees_df['Mentee'].unique()]
# Verify counts
print("Number of unique mentors:", len(mentors_prefixed))
print("Number of unique unmatched mentees:", len(mentees_prefixed))

# Add prefixed nodes
B2.add_nodes_from(mentors_prefixed, bipartite=0)
B2.add_nodes_from(mentees_prefixed, bipartite=1)

# Add edges with prefixed node identifiers
for idx, row in match_scores_df.iterrows():
    mentor = 'mentor_' + str(row['Mentor'])
    mentee = 'mentee_' + str(row['Mentee'])
    if mentee in mentees_prefixed:  # Check if mentee is among unmatched
        match_score = row['Match Score']
        B2.add_edge(mentor, mentee, weight=-match_score)
    
print("B2 nodes and edge:",B2)
# After adding all edges
print("Total edges in the graph:", B2.number_of_edges())

# Obtain the minimum weight full matching
matching = bipartite.matching.minimum_weight_full_matching(B2, weight='weight')

# Correctly extract match scores and include them in the result
new_match_results = []
for mentor, mentee in matching.items():
    if mentor in B2 and mentee in B2 and B2.nodes[mentor]['bipartite'] == 0:
        # Retrieve the original match score (invert the negative weight stored in the graph)
        match_score = -B2[mentor][mentee]['weight']
        mentor_cleaned = mentor.replace('mentor_', '')  # Clean mentor prefix
        mentee_cleaned = mentee.replace('mentee_', '')  # Clean mentee prefix
        new_match_results.append({
            'Mentor': mentor_cleaned,
            'Mentee': mentee_cleaned,
            'Match Score': match_score
        })

# Convert the new match results to a DataFrame
new_matches_df = pd.DataFrame(new_match_results)

# Use pd.concat to append new matches to the existing final_matches_df
final_matches_df = pd.concat([final_matches_df, new_matches_df], ignore_index=True)

# Sort the updated DataFrame by 'Match Score' descending, then 'Mentor' and 'Mentee' ascending
final_matches_df = final_matches_df.sort_values(by=['Match Score', 'Mentor', 'Mentee'], ascending=[False, True, True])

# Reset index if necessary
final_matches_df.reset_index(drop=True, inplace=True)

# Output the results
print('Exporting match_2.3_matches.csv')
print(final_matches_df.head())
final_matches_df.to_csv('match_2.3_matches.csv', index=False)

# Count unique mentors and mentees who got matched
unique_mentors_matched = final_matches_df['Mentor'].nunique()
unique_mentees_matched = final_matches_df['Mentee'].nunique()

print(f"Number of mentors who got final matched: {unique_mentors_matched}")
print(f"Number of mentees who got final matched: {unique_mentees_matched}")


# Group by 'Mentor' and count the number of 'Mentee'
mentor_mentee_counts = final_matches_df.groupby('Mentor').size().reset_index(name='Mentee Count')
# Count how many mentors have exactly 1, 2, or 3 mentees
mentee_distribution = mentor_mentee_counts['Mentee Count'].value_counts().sort_index()
print("Distribution of Mentees per Mentor:")
print(mentee_distribution)

# Optionally, to make it more descriptive:
for mentee_count in [1, 2, 3]:
    num_mentors = mentee_distribution.get(mentee_count, 0)
    print(f"Mentors with {mentee_count} mentee(s): {num_mentors}")


mentee_distribution.plot(kind='bar')
plt.title('Distribution of Mentees per Mentor')
plt.xlabel('Number of Mentees')
plt.ylabel('Number of Mentors')
plt.xticks(ticks=[0, 1, 2], labels=['1 Mentee', '2 Mentees', '3 Mentees'], rotation=0)  # Adjust labels based on actual data
plt.show()

