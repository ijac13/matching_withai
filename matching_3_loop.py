import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

#### repeat match with mentors and unmatched mentees after the first match, until every mentee has a mentor

# Load the DataFrame
match_scores_df = pd.read_csv('match_1.5_score.csv')

# Initialize the DataFrame to store final match results
final_matches_df = pd.DataFrame()

# Keep track of unmatched mentees
unmatched_mentees = set(match_scores_df['Mentee'].unique())

while unmatched_mentees:
    # Initialize the graph
    B = nx.Graph()

    # Add nodes
    mentors_prefixed = ['mentor_' + str(mentor) for mentor in match_scores_df['Mentor'].unique()]
    mentees_prefixed = ['mentee_' + str(mentee) for mentee in unmatched_mentees]

    B.add_nodes_from(mentors_prefixed, bipartite=0)
    B.add_nodes_from(mentees_prefixed, bipartite=1)

    # Add edges
    for idx, row in match_scores_df[match_scores_df['Mentee'].isin(unmatched_mentees)].iterrows():
        mentor = 'mentor_' + str(row['Mentor'])
        mentee = 'mentee_' + str(row['Mentee'])
        match_score = row['Match Score']
        B.add_edge(mentor, mentee, weight=-match_score)

    # Perform matching
    matching = bipartite.matching.minimum_weight_full_matching(B, weight='weight')

    # Extract results
    match_results = []
    for mentor, mentee in matching.items():
        if mentor in B and mentee in B and B.nodes[mentor]['bipartite'] == 0:
            match_score = -B[mentor][mentee]['weight']
            mentor_cleaned = mentor.replace('mentor_', '')
            mentee_cleaned = mentee.replace('mentee_', '')
            match_results.append({
                'Mentor': mentor_cleaned,
                'Mentee': mentee_cleaned,
                'Match Score': match_score
            })

    # Update the DataFrame with new matches
    new_matches_df = pd.DataFrame(match_results)
    final_matches_df = pd.concat([final_matches_df, new_matches_df], ignore_index=True)

    # Update the set of unmatched mentees
    matched_mentees = set(new_matches_df['Mentee'])
    unmatched_mentees = unmatched_mentees - matched_mentees

    # Break if no matches were made in this round
    if new_matches_df.empty:
        break

# Final sorting and cleaning
final_matches_df = final_matches_df.sort_values(by=['Match Score', 'Mentor', 'Mentee'], ascending=[False, True, True])
final_matches_df.reset_index(drop=True, inplace=True)

# Output the final matches
final_matches_df.to_csv('match_3_matches.csv', index=False)
print('Final matching results exported to "match_3_matche.csv".')

# Analyze the distribution of mentees per mentor
mentor_mentee_counts = final_matches_df.groupby('Mentor').size()
mentee_distribution = mentor_mentee_counts.value_counts().sort_index()
# print("Distribution of Mentees per Mentor:")
# print(mentee_distribution)

for count, num_mentors in mentee_distribution.items():
    print(f"Mentors with {count} mentee(s): {num_mentors}")

# Verify counts
print("Number of unique mentors:", len(final_matches_df['Mentor'].unique()))
print("Number of unique mentees:", len(final_matches_df['Mentee'].unique()))