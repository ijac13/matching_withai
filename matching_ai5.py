import pandas as pd #Python Data Analysis Library
import matplotlib.pyplot as plt # Visualization with Python
import numpy as np
import ast
import networkx as nx
from datetime import datetime

# Step 1: Data Preparation
#1.1 Load the data
mentors_df = pd.read_csv('Mentor_Submissions.csv')
mentees_df = pd.read_csv('Mentee_Submissions.csv')
no_reply_df = pd.read_csv('No-Reply_list.csv')  

# # Check existing columns
print('Check existing columns')
print("Mentor DataFrame columns:", mentors_df.columns)
print("Mentee DataFrame columns:", mentees_df.columns)
print("No-Reply DataFrame columns:", no_reply_df.columns)

# Check and rename the column if necessary
if 'Email' in no_reply_df.columns:
    no_reply_df.rename(columns={'Email': 'Coda Email'}, inplace=True)

#1.2 Clean the Data
# 1. Exclude test data
# 2. Include people who are in the current cohort
current_cohort = 'Spring 2025' ##update t

mentors_df = mentors_df[(mentors_df['Test content'] == False) 
                        & (mentors_df['Cohort'] == current_cohort)]
mentees_df = mentees_df[(mentees_df['Test content'] == False) 
                        & (mentees_df['Cohort'] == current_cohort)]
print('Current cohort raw submissions ---')
print(f"Mentor submissions: {len(mentors_df)}")
print(f"Mentee submissions: {len(mentees_df)}")

# 3. Strip leading/trailing spaces and convert to lower case for consistency
mentors_df['Coda Email'] = mentors_df['Coda Email'].str.strip().str.lower()
mentees_df['Coda Email'] = mentees_df['Coda Email'].str.strip().str.lower()
no_reply_df['Coda Email'] = no_reply_df['Coda Email'].str.strip().str.lower()  

# 4. Remove duplicates on 'Coda Email' field and keep='first' to keep the first occurrence.
mentors_df = mentors_df.drop_duplicates(subset=['Coda Email'], keep='first')
mentees_df = mentees_df.drop_duplicates(subset=['Coda Email'], keep='first')

# 5. Select only the necessary columns
mentors_df = mentors_df[['Coda Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Important Attribute - First','Important Attribute - Second','Important Attribute - Third', 
                         'Open Answer', 'Full Name', 'Avg Year of YOE']]
mentees_df = mentees_df[['Coda Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Important Attribute - First','Important Attribute - Second','Important Attribute - Third', 
                         'Open Answer', 'Full Name', 'Avg Year of YOE', 'Apply mentor']]
no_reply_df = no_reply_df[['Coda Email']]

# 6. Set 'Coda Email' as the index
mentors_df.set_index('Coda Email', inplace=True)
mentees_df.set_index('Coda Email', inplace=True)
no_reply_df.set_index('Coda Email', inplace=True)

# Print clean result
print('Current cohort total submissions ---')
print(f"Mentor submissions: {len(mentors_df)}")
print(f"Mentee submissions: {len(mentees_df)}")

#1.3 Filter data
# 1. Include only those who have committed
# 2. Print emails that are in no-reply list or not commit
filtered_out_mentors = mentors_df[(mentors_df['Participation Commitment'] != 'Yes') | 
                                  mentors_df.index.isin(no_reply_df.index)]
filtered_out_mentees = mentees_df[(mentees_df['Participation Commitment'] != 'Yes') | 
                                  mentees_df.index.isin(no_reply_df.index)]

# Print the filtered out emails for mentors and mentees
print("Filtered out mentor emails:")
print(filtered_out_mentors.index.tolist())  # Prints list of email addresses

print("Filtered out mentee emails:")
print(filtered_out_mentees.index.tolist())  # Prints list of email addresses

# 3. Exclude from no-reply list
mentors_df = mentors_df[(mentors_df['Participation Commitment'] == 'Yes') 
                                  & ~mentors_df.index.isin(no_reply_df.index)]
mentees_df = mentees_df[(mentees_df['Participation Commitment'] == 'Yes') 
                                  & ~mentees_df.index.isin(no_reply_df.index)]

# Print filter result
print('Current cohort total submissions after filter no-reply list ---')
print(f"Mentor submissions: {len(mentors_df)}")
print(f"Mentee submissions: {len(mentees_df)}")

#1.4 Prepare data
# 1. Remove Unnecessary Columns
mentors_df.drop(columns=['Participation Commitment'], inplace=True)
mentees_df.drop(columns=['Participation Commitment'], inplace=True)

# Check existing columns
print('Check existing columns')
print("Mentor DataFrame columns:", mentors_df.columns)
print("Mentee DataFrame columns:", mentees_df.columns)

# 2. Convert 'Open Answer' to Boolean
mentors_df['Open Answer'] = mentors_df['Open Answer'].apply(lambda x: bool(x) and not pd.isna(x))
mentees_df['Open Answer'] = mentees_df['Open Answer'].apply(lambda x: bool(x) and not pd.isna(x))

# 3. Ensure Numeric Fields Are Correctly Formatted
# Check type of each column
print("Mentors columns:", mentors_df.info())
print("Mentees columns:", mentees_df.info())

# List of columns that contain comma-separated lists
list_columns = ['In-Person Meeting Location', 'Roles', 'Industry', 'Company Stage', 'Topics', 'Important Attribute - First','Important Attribute - Second','Important Attribute - Third']

# # Loop through each column and split the comma-separated strings into lists
# 4. Clean 'Important Attribute' columns by keeping only the first answer
important_attribute_columns = ['Important Attribute - First', 'Important Attribute - Second', 'Important Attribute - Third']

for column in important_attribute_columns:
    mentors_df[column] = mentors_df[column].apply(lambda x: x.split(',')[0] if pd.notnull(x) else None)
    mentees_df[column] = mentees_df[column].apply(lambda x: x.split(',')[0] if pd.notnull(x) else None)

# 5. Combine 'Important Attribute' columns into one and maintain their order
def combine_attributes(row):
    # Extract the attributes, ignoring 'None'
    attributes = [row['Important Attribute - First'], row['Important Attribute - Second'], row['Important Attribute - Third']]
    filtered_attributes = [attr for attr in attributes if attr is not None]

    # Join the filtered attributes with a chosen separator (e.g., ', ')
    combined_attributes = ', '.join(filtered_attributes)
    return combined_attributes

# Apply the function to each row in both dataframes
mentors_df['Most Important Attributes'] = mentors_df.apply(combine_attributes, axis=1)
mentees_df['Most Important Attributes'] = mentees_df.apply(combine_attributes, axis=1)

# Optionally, you can drop the original 'Important Attribute' columns if they are no longer needed
mentors_df.drop(columns=['Important Attribute - First', 'Important Attribute - Second', 'Important Attribute - Third'], inplace=True)
mentees_df.drop(columns=['Important Attribute - First', 'Important Attribute - Second', 'Important Attribute - Third'], inplace=True)


# Export the first 10 rows to CSV files
mentors_df.head(10).to_csv('processed_sample_mentors.csv', index=True)
mentees_df.head(10).to_csv('processed_sample_mentees.csv', index=True)

#Step 2: Define Weighting System
#2.1 Decide weighting system
#Combining Penalty and Rewarding Systems

#2.2 Analysis Offset to "decide" a threshold for maximum allowed difference
# Export csv for offset analysis
mentors_df.to_csv('mentors_offset_analysis.csv', index=True)
mentees_df.to_csv('mentees_offset_analysis.csv', index=True)
# use offset_analysis.py to make the decision

#Step 3: Algorithm Design
#3.1 Initial Matching
# Initialize an empty list to store match information
match_info = []

# Define the offset threshold
offset_threshold = 6  # Define the threshold based on the result from offse_analysis.py 

# Define rewards and penalties 
offset_reward = 100  # Reward for offset within the threshold
offset_penalty = -100  # Penalty for offset beyond the threshold
yoe_reward_ideal = 150  # Reward for YOE difference of 2-3 years
yoe_reward_good = 120  # Reward for YOE difference of 4-8 years
yoe_reward_minimal = 20  # Minimal reward for YOE difference of >8 years


#3.2 Hard Constraints
# Iterate over each mentor-mentee pair
for mentor_email, mentor_row in mentors_df.iterrows():
    for mentee_email, mentee_row in mentees_df.iterrows():
        
        # Initialize match score
        match_score = 0
        offset_score = 0
        yoe_scroe = 0

        # Calculate offset difference and apply rewards/penalties
        offset_diff = abs(mentor_row['Offset'] - mentee_row['Offset'])
        if offset_diff <= offset_threshold:
            offset_score = offset_reward
        else:
            offset_score = offset_penalty
        match_score += offset_score

        # Calculate YOE difference and apply rewards
        yoe_diff = mentor_row['Avg Year of YOE'] - mentee_row['Avg Year of YOE']
        if yoe_diff <= 0:
            continue  # Skip pairs where mentor's YOE is not greater than mentee's YOE
        elif yoe_diff >= 2 and yoe_diff <= 3:
            yoe_score = yoe_reward_ideal
        elif yoe_diff >= 4 and yoe_diff <= 8:
            yoe_score = yoe_reward_good
        elif yoe_diff > 8:
            yoe_score = yoe_reward_minimal
        match_score += yoe_score


        # Store the match information including the contributions of each criterion
        match_info.append({
            'Mentor': mentor_email,
            'Mentee': mentee_email,
            'Offset Difference': offset_diff,
            'Offset Score': offset_score,
            'YOE Difference': yoe_diff,
            'YOE Score': yoe_score,
            'Match Score': match_score
        })

# Convert the match information into a DataFrame for further analysis
match_scores_df = pd.DataFrame(match_info)

# Assuming 'Mentor' and 'Match Score' are the column names in your DataFrame
match_scores_df = match_scores_df.sort_values(by=['Mentor', 'Match Score'], ascending=[True, False])


# Export csv for hard constraints
print('export match_1_constraints.csv')
match_scores_df.to_csv('match_1_constraints.csv')

# Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()
unique_mentees_matched = match_scores_df['Mentee'].nunique()

print(f"Number of mentors who got matched for match_1: {unique_mentors_matched}")
print(f"Number of mentees who got matched for match_1: {unique_mentees_matched}")

# After each match stage, add detailed statistics
def print_match_statistics(df, stage_name):
    print(f"\n=== {stage_name} Statistics ===")
    print(f"Total matches found: {len(df)}")
    print(f"Unique mentors: {df['Mentor'].nunique()}")
    print(f"Unique mentees: {df['Mentee'].nunique()}")
    print(f"Average match score: {df['Match Score'].mean():.2f}")
    print(f"Score range: {df['Match Score'].min():.2f} to {df['Match Score'].max():.2f}")
    print("Sample of top 5 matches:")
    print(df.head())
    print("=" * 50)

# Add these calls after each matching stage
print_match_statistics(match_scores_df, "Match 1 - Hard Constraints")
match_scores_df.to_csv('match_1_constraints.csv')

#3.3 Reward the overlapping by Most important Attributes
# Define the base score for an overlap
base_overlap_score = 20
# Additional rewards based on ranking in 'Most Important Attributes'
importance_weights = [5, 3, 2]

# 1. Define a parsing function that splits a string on commas and strips any extra whitespace around the attribute names
def parse_comma_separated_list(value):
    if pd.isna(value) or value.strip() == '':
        return []
    # Split the string by comma and strip spaces from each resulting item
    return [item.strip() for item in value.split(',')]

attributes_columns = ['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']
importance_columns = ['Most Important Attributes']  

# Apply the parsing for both mentors and mentees DataFrames
for column in attributes_columns + importance_columns:
    mentors_df[column] = mentors_df[column].apply(parse_comma_separated_list)
    mentees_df[column] = mentees_df[column].apply(parse_comma_separated_list)

#debug
# print(mentors_df['Most Important Attributes'].head())
# print(mentees_df['Most Important Attributes'].head())


# 2. Define the Scoring Function
def calculate_overlap_and_score(mentor_attrs, mentee_attrs, mentor_importance, mentee_importance, importance_weights, base_overlap_score):
    score = 0
    total_overlaps = 0
    
    # Specify the emails of the mentor and mentee you want to debug
    # debug_mentor_email = 'mentor@gmail.com'
    # debug_mentee_email = 'mentee@gmail.com'

    for attr in ['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']:
      # Check if either party has "No Preference" for this attribute
        # if "No Preference" in mentor_attrs.get(attr, []) or "No Preference" in mentee_attrs.get(attr, []):
        #     continue  # Skip this attribute

        mentor_set = set(mentor_attrs.get(attr, []))
        mentee_set = set(mentee_attrs.get(attr, []))
        overlap = mentor_set.intersection(mentee_set)
        overlap_count = len(overlap)
        #debug
        # print(f"Checking {attr}: Mentor - {mentor_set}, Mentee - {mentee_set}, Overlap - {overlap}")
        # print(f"Checking overlap_count: {overlap_count}")
        
        # Print detailed information for the specified mentor and mentee
        # if mentor_email == debug_mentor_email and mentee_email == debug_mentee_email:
            # print(f"Checking {attr}: Mentor - {mentor_set}, Mentee - {mentee_set}, Overlap - {overlap}, overlap_count: {overlap_count}")

        if overlap_count > 0:
            total_overlaps += overlap_count
            current_score = base_overlap_score * overlap_count
            rank = -1  # Initialize rank with a default or placeholder value
            weight = 1  # Default weight if no importance is found

            if attr in mentor_importance:
                rank = mentor_importance.index(attr)
                weight = importance_weights[rank]
                current_score *= weight
                #debug
                # print(f"Mentor importance applied: {attr} at rank {rank} with weight {weight}")
                # Print detailed information for the specified mentor and mentee
                
            if attr in mentee_importance:
                rank = mentee_importance.index(attr)
                weight = importance_weights[rank]
                current_score *= weight
                #debug
                # print(f"Mentee importance applied: {attr} at rank {rank} with weight {weight}")
         

            score += current_score
            #debug
            # print("score:", score, total_overlaps)
            # if mentor_email == debug_mentor_email and mentee_email == debug_mentee_email:
              # print(f"Mentor Checking {attr}: rank - {rank}, weight - {weight}, current_score - {current_score}")

    return score, total_overlaps

# 3. Pair Mentors and Mentees and Calculate Scores
# If match_scores_df does not already contain the columns, initialize them
needed_columns = ['Total Overlaps', 'Overlap Score', 'Match Score']
for column in needed_columns:
    if column not in match_scores_df.columns:
        if column == 'Total Overlaps':
            match_scores_df[column] = 0  # Initialize as integer
        else:
            match_scores_df[column] = 0.0  # Initialize as float for other scores

# Convert types explicitly to ensure consistency
match_scores_df['Total Overlaps'] = match_scores_df['Total Overlaps'].astype(int)
match_scores_df['Overlap Score'] = match_scores_df['Overlap Score'].astype(float)
match_scores_df['Match Score'] = match_scores_df['Match Score'].astype(float)


for mentor_email in mentors_df.index:
    for mentee_email in mentees_df.index:
        mentor_data = mentors_df.loc[mentor_email]
        mentee_data = mentees_df.loc[mentee_email]

        score, total_overlaps = calculate_overlap_and_score(
            mentor_data[['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']].to_dict(),
            mentee_data[['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']].to_dict(),
            mentor_data['Most Important Attributes'],
            mentee_data['Most Important Attributes'],
            importance_weights,
            base_overlap_score
        )

        # Find or create the match entry in match_scores_df
        match_index = match_scores_df[(match_scores_df['Mentor'] == mentor_email) & (match_scores_df['Mentee'] == mentee_email)].index
        if match_index.empty:
            # If no existing match, use pd.concat to append new row
            new_row = pd.DataFrame([{
                'Mentor': mentor_email,
                'Mentee': mentee_email,
                'Total Overlaps': total_overlaps,
                'Overlap Score': score,
                'Match Score': score
            }])
            match_scores_df = pd.concat([match_scores_df, new_row], ignore_index=True)
        else:
            # Update existing match with new scores
            idx = match_index[0]
            match_scores_df.at[idx, 'Total Overlaps'] += total_overlaps
            #debug 
            # print(f"Before update: {match_scores_df.at[match_index[0], 'Sum Importance Weights']}")
            #debug
            # print(f"After update: {match_scores_df.at[match_index[0], 'Sum Importance Weights']}")
            match_scores_df.at[idx, 'Overlap Score'] += score
            match_scores_df.at[idx, 'Match Score'] += score


# Define the new column order
new_column_order = [
    'Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 
    'YOE Difference', 'YOE Score', 'Total Overlaps', 
    'Overlap Score', 'Match Score'
]

# Reorder the DataFrame columns
match_scores_df = match_scores_df[new_column_order]

# Debug and save updated DataFrame
print(match_scores_df.head())
# print(match_scores_df.describe())  # Provides summary statistics
match_scores_df.to_csv('match_2_overlaps.csv', index=False)

# Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()
unique_mentees_matched = match_scores_df['Mentee'].nunique()

print(f"Number of mentors who got matched for match_2: {unique_mentors_matched}")
print(f"Number of mentees who got matched for match_2: {unique_mentees_matched}")

print_match_statistics(match_scores_df, "Match 2 - Overlaps")
match_scores_df.to_csv('match_2_overlaps.csv')

#3.4 Reward people who write Open Answer
# Convert Open Answer to string, assuming NaNs or None should be treated as not provided
mentors_df['Open Answer'] = mentors_df['Open Answer'].astype(str).fillna('')
mentees_df['Open Answer'] = mentees_df['Open Answer'].astype(str).fillna('')

# Define the reward for providing an open answer
open_answer_reward = 50

# Ensure 'Open Answer Score' column exists in match_scores_df
match_scores_df['Open Answer Score'] = 0

# Loop through each match to update the score based on the provision of an open answer
for idx, match in match_scores_df.iterrows():
    mentor_email = match['Mentor']
    mentee_email = match['Mentee']

    mentor_row = mentors_df.loc[mentor_email]
    mentee_row = mentees_df.loc[mentee_email]

    # Check if an open answer was provided by the mentor or mentee
    if mentor_row['Open Answer'].strip() or mentee_row['Open Answer'].strip():
        # Add the open answer reward to the open answer score and update match score
        match_scores_df.at[idx, 'Open Answer Score'] += open_answer_reward
        match_scores_df.at[idx, 'Match Score'] += open_answer_reward

    #debug
    # print(match_scores_df[['Mentor', 'Mentee', 'Open Answer Score', 'Match Score']].head())


# Reorder columns to ensure 'Match Score' is the last column
final_columns_order =  ['Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 
                        'YOE Difference', 'YOE Score', 'Total Overlaps', 
                        'Overlap Score', 'Open Answer Score', 'Match Score']
match_scores_df = match_scores_df[final_columns_order]

# Export csv
print('export match_3_openanswer.csv')
print(match_scores_df.head())
match_scores_df.to_csv('match_3_openanswer.csv')
# Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()
unique_mentees_matched = match_scores_df['Mentee'].nunique()

print(f"Number of mentors who got matched for match_3: {unique_mentors_matched}")
print(f"Number of mentees who got matched for match_3: {unique_mentees_matched}")

print_match_statistics(match_scores_df, "Match 3 - Open Answers")
match_scores_df.to_csv('match_3_openanswer.csv')

#3.5 Rewarding Mentees Who Applied to Be Mentors
# Initialize the 'Apply Mentor Score' column in match_scores_df if it doesn't exist
match_scores_df['Apply Mentor Score'] = 0

# Define the reward for mentees who have also applied to be mentors
mentee_apply_mentor_reward = 30

# Loop through each match to update the score based on whether the mentee has applied to be a mentor
for idx, match in match_scores_df.iterrows():
    mentee_email = match['Mentee']

    # Retrieve the mentee row from mentees_df
    mentee_row = mentees_df.loc[mentee_email]

    # Check if the mentee has applied to be a mentor
    if mentee_row['Apply mentor'] == 'Yes':  # Assuming the column is named 'Apply mentor' and contains 'Yes' if applied
        # Add the apply mentor reward to the apply mentor score and update match score
        match_scores_df.at[idx, 'Apply Mentor Score'] += mentee_apply_mentor_reward
        match_scores_df.at[idx, 'Match Score'] += mentee_apply_mentor_reward

# Ensure 'Match Score' is the last column by setting the column order
final_columns_order =  ['Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 
                        'YOE Difference', 'YOE Score', 'Total Overlaps', 
                        'Overlap Score', 'Open Answer Score', 'Apply Mentor Score', 'Match Score']
match_scores_df = match_scores_df[final_columns_order]
# Export csv 
print('export match_4_applymentor.csv')
print(match_scores_df.head())
match_scores_df.to_csv('match_4_applymentor.csv')
# Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()
unique_mentees_matched = match_scores_df['Mentee'].nunique()

print(f"Number of mentors who got matched for match_4: {unique_mentors_matched}")
print(f"Number of mentees who got matched for match_4: {unique_mentees_matched}")

print_match_statistics(match_scores_df, "Match 4 - Apply Mentor")
match_scores_df.to_csv('match_4_applymentor.csv')

# Step 4: Maximize Matches while ensuring each mentee is matched with only one mentor

# 1. Prepare the Score Lookup Dictionary
# Creating a lookup dictionary for match scores for faster access
score_lookup = {(row['Mentor'], row['Mentee']): row['Match Score'] for index, row in match_scores_df.iterrows()}

#debug
print(mentors_df.index.duplicated().sum())  # Check for duplicate mentor emails
print("Total mentor opportunities (including duplicates):", len(mentors_df.index) * 3)
print("Total mentees available:", len(mentees_df.index))



# 2.Create a new bipartite graph
# Create a new bipartite graph
B = nx.Graph()

# Adding mentor nodes - duplicating each mentor node 3 times to allow up to 3 matches
for email in mentors_df.index:  # Use DataFrame index directly
    for i in range(1, 4):  # Create 3 duplicates for each mentor
        B.add_node(f"{email}_{i}", bipartite=0)  # Mentor nodes

# Add mentee nodes using the index
B.add_nodes_from(mentees_df.index, bipartite=1)  # Mentee nodes

# Add edges using the negative weight for max weight matching
for index, row in match_scores_df.iterrows():
    for i in range(1, 4):
        B.add_edge(f"{row['Mentor']}_{i}", row['Mentee'], weight=-row['Match Score'])
#debug
print("Total edges in the graph:", B.number_of_edges())


# 3. Process the Maximum Matching
# Find the maximum matching using the Hopcroft-Karp algorithm
matching = nx.algorithms.bipartite.maximum_matching(B, top_nodes={f"{email}_{i}" for email in mentors_df.index for i in range(1, 4)})


# Filter to include only mentor to mentee matches and clean up the mentor identifiers
final_matching = {ment.split('_')[0]: mentee for ment, mentee in matching.items() if ment in B.nodes() and B.nodes[ment]['bipartite'] == 0}

# 4. Lookup Match Score
# Creating a lookup dictionary for match scores for faster access
score_lookup = {(row['Mentor'], row['Mentee']): row['Match Score'] for index, row in match_scores_df.iterrows()}

# Using the lookup dictionary to fetch scores
match_results = [
    {'Mentor': mentor.split('_')[0], 'Mentee': mentee, 'Match Score': score_lookup[(mentor.split('_')[0], mentee)]}
    for mentor, mentee in final_matching.items() if (mentor.split('_')[0], mentee) in score_lookup
]


# 5. Create Match Results with Scores
# Using the lookup dictionary to fetch scores
match_results = [
    {'Mentor': mentor, 'Mentee': mentee, 'Match Score': score_lookup[(mentor, mentee)]}
    for mentor, mentee in final_matching.items() if (mentor, mentee) in score_lookup
]


# 6. Convert to DataFrame and Sort
# Convert to DataFrame
final_matches_df = pd.DataFrame(match_results)

# Sort by Match Score DESC, then Mentor and Mentee ASC
final_matches_df = final_matches_df.sort_values(by=['Match Score', 'Mentor', 'Mentee'], ascending=[False, True, True])

# 7. Output
print('Exporting match_5_matches.csv')
print(final_matches_df.head())
final_matches_df.to_csv('match_5_matches.csv', index=False)

# Count unique mentors who got matched
unique_mentors_matched = final_matches_df['Mentor'].nunique()
unique_mentees_matched = final_matches_df['Mentee'].nunique()

print(f"Number of mentors who got matched for match_5: {unique_mentors_matched}")
print(f"Number of mentees who got matched for match_5: {unique_mentees_matched}")

print_match_statistics(final_matches_df, "Match 5 - Final Matches")
final_matches_df.to_csv('match_5_matches.csv', index=False)

# Add a final summary
print("\n=== Final Matching Summary ===")
print(f"Initial pool: {len(mentors_df)} mentors and {len(mentees_df)} mentees")
print(f"Final matches made: {len(final_matches_df)}")
print(f"Mentors matched: {final_matches_df['Mentor'].nunique()}")
print(f"Mentees matched: {final_matches_df['Mentee'].nunique()}")
print("=" * 50)

# Check for negative match scores
negative_scores = match_scores_df[match_scores_df['Match Score'] < 0]

if not negative_scores.empty:
    print("There are negative match scores.")
    print(negative_scores)
else:
    print("n/a")
    

## add unmatched mentees
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

# Output the new matches with scores in the desired format

print("Mentor\tMentee\tMatch Score")
for mentor, (mentee, score) in new_matches.items():
    print(f"{mentor}\t{mentee}\t{score}")

# Convert the dictionary to a DataFrame with the correct columns
new_matches_df = pd.DataFrame(
    [(mentor, mentee, score) for mentor, (mentee, score) in new_matches.items()],
    columns=['Mentor', 'Mentee', 'Match Score']
)

# Combine with initial matches if needed
final_matches_df = pd.concat([initial_matches_df, new_matches_df], ignore_index=True)

# Ensure the final DataFrame has the correct structure
final_matches_df = final_matches_df[['Mentor', 'Mentee', 'Match Score']]

# Save the final matches to a new CSV with the correct columns
final_matches_df.to_csv('match_6_addmentee.csv', index=False)

# Add a final summary
print("\n=== Final Matching Summary ===")
print(f"Initial pool: {len(mentors_df)} mentors and {len(mentees_df)} mentees")
print(f"Final matches made: {len(final_matches_df)}")
print(f"Mentors matched: {final_matches_df['Mentor'].nunique()}")
print(f"Mentees matched: {final_matches_df['Mentee'].nunique()}")

# Calculate unmatched mentors and mentees
unmatched_mentors = len(mentors_df) - final_matches_df['Mentor'].nunique()
unmatched_mentees = len(mentees_df) - final_matches_df['Mentee'].nunique()

print(f"Unmatched mentors: {unmatched_mentors}")
print(f"Unmatched mentees: {unmatched_mentees}")

# Calculate average match score
average_match_score = final_matches_df['Match Score'].mean()
print(f"Average match score: {average_match_score:.2f}")

print("=" * 50)