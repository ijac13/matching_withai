import pandas as pd

# Load the initial match results
initial_matches_df = pd.read_csv('match_5_matches.csv')

# Assuming match_scores_df is your DataFrame containing all possible match scores
# Example structure: ['Mentor', 'Mentee', 'Match Score']

# Identify unmatched mentees
all_mentees = set(match_scores_df['Mentee'].unique())
matched_mentees = set(initial_matches_df['Mentee'].unique())
unmatched_mentees = all_mentees - matched_mentees

# Filter match scores for unmatched mentees
unmatched_mentee_scores = match_scores_df[match_scores_df['Mentee'].isin(unmatched_mentees)]

# Create a dictionary to store new matches for each mentor
new_matches = {}

# Iterate over each unique mentor
for mentor in unmatched_mentee_scores['Mentor'].unique():
    # Filter the DataFrame for the current mentor
    mentor_matches = unmatched_mentee_scores[unmatched_mentee_scores['Mentor'] == mentor]
    
    # Sort potential mentees by match score in descending order
    sorted_matches = mentor_matches.sort_values(by='Match Score', ascending=False)
    
    # Select the top candidate
    if not sorted_matches.empty:
        top_mentee = sorted_matches.iloc[0]['Mentee']
        top_score = sorted_matches.iloc[0]['Match Score']
        new_matches[mentor] = (top_mentee, top_score)

# Output the new matches with scores
print("Mentor\tMentee\tMatch Score")
for mentor, (mentee, score) in new_matches.items():
    print(f"{mentor}\t{mentee}\t{score}")

# Optionally, you can create a new DataFrame for these new matches
new_matches_df = pd.DataFrame(list(new_matches.items()), columns=['Mentor', 'Mentee', 'Match Score'])

# Combine with initial matches if needed
final_matches_df = pd.concat([initial_matches_df, new_matches_df], ignore_index=True)

# Save the final matches to a new CSV
final_matches_df.to_csv('match_6_addmentee.csv', index=False)