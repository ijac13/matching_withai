import pandas as pd #Python Data Analysis Library
import matplotlib.pyplot as plt # Visualization with Python
import numpy as np

# Step 1: Data Preparation
# 1.1 Load the data
mentors_df = pd.read_csv('Mentor_Submissions.csv')
mentees_df = pd.read_csv('Mentee_Submissions.csv')
no_reply_df = pd.read_csv('No-Reply_list.csv')  

# # Check existing columns
# print('Check existing columns')
# print("Mentor DataFrame columns:", mentors_df.columns)
# print("Mentee DataFrame columns:", mentees_df.columns)
# print("No-Reply DataFrame columns:", no_reply_df.columns)

# 1.2 Clean the Data
# 1. Exclude test data
# 2. Include people who are in the current cohort
current_cohort = 'Fall 2023'

mentors_df = mentors_df[(mentors_df['Test content'] != 'true') 
                        & (mentors_df['Cohort'] == current_cohort)]
mentees_df = mentees_df[(mentees_df['Test content'] != 'true') 
                        & (mentees_df['Cohort'] == current_cohort)]

# 3. Strip leading/trailing spaces and convert to lower case for consistency
mentors_df['Email'] = mentors_df['Email'].str.strip().str.lower()
mentees_df['Email'] = mentees_df['Email'].str.strip().str.lower()
no_reply_df['Email'] = no_reply_df['Email'].str.strip().str.lower()  

# 4. Remove duplicates on 'Email' field and keep='first' to keep the first occurrence.
mentors_df = mentors_df.drop_duplicates(subset=['Email'], keep='first')
mentees_df = mentees_df.drop_duplicates(subset=['Email'], keep='first')

# 5. Select only the necessary columns
mentors_df = mentors_df[['Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Most Important Attribute', 
                         'Open Answer', 'Full Name', 'Avg Year of YOE']]
mentees_df = mentees_df[['Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Most Important Attribute', 
                         'Open Answer', 'Full Name', 'Avg Year of YOE', 'Apply mentor']]
no_reply_df = no_reply_df[['Email']]

# 6. Set 'Email' as the index
mentors_df.set_index('Email', inplace=True)
mentees_df.set_index('Email', inplace=True)

# Print clean result
print('Current cohort total submissions ---')
print(f"Mentor submissions: {len(mentors_df)}")
print(f"Mentee submissions: {len(mentees_df)}")

# 1.3 Filter data
# 1. Include only those who have committed
# 2. Exclude from no-reply list

mentors_df = mentors_df[(mentors_df['Participation Commitment'] == 'Yes')
                        & ~mentors_df.index.isin(no_reply_df['Email'])]
mentees_df = mentees_df[(mentees_df['Participation Commitment'] == 'Yes')
                        & ~mentees_df.index.isin(no_reply_df['Email'])]

# Print filter result
print('Current cohort total submissions after filter ---')
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
print("No-Reply DataFrame columns:", no_reply_df.columns)

# 2. Convert 'Open Answer' to Boolean
mentors_df['Open Answer'] = mentors_df['Open Answer'].apply(lambda x: bool(x) and not pd.isna(x))
mentees_df['Open Answer'] = mentees_df['Open Answer'].apply(lambda x: bool(x) and not pd.isna(x))

# 3. Ensure Numeric Fields Are Correctly Formatted
# Check type of each column
print("Mentors columns:", mentors_df.info())
print("Mentees columns:", mentees_df.info())


# List of columns that contain comma-separated lists
list_columns = ['In-Person Meeting Location', 'Roles', 'Industry', 'Company Stage', 'Topics', 'Most Important Attribute']

# Loop through each column and split the comma-separated strings into lists
for column in list_columns:
    mentors_df[column] = mentors_df[column].apply(lambda x: x.split(',') if pd.notnull(x) else [])
    mentees_df[column] = mentees_df[column].apply(lambda x: x.split(',') if pd.notnull(x) else [])

# # Export the first 10 rows to CSV files
# mentors_df.head(10).to_csv('processed_mentors_sample.csv', index=True)
# mentees_df.head(10).to_csv('processed_mentees_sample.csv', index=True)

#Step 2: Define Weighting System
#2.1 Decide weighting system
#Combining Penalty and Rewarding Systems

#2.2 Analysis Offset to “decide” a threshold for maximum allowed difference
# Export csv for offset analysis
mentors_df.to_csv('mentors_offset_analysis.csv', index=True)
mentees_df.to_csv('mentees_offset_analysis.csv', index=True)
# use offset_analysis.py to make the decision


#Step 3: Algorithm Design
#3.1 Initial Matching
# Initialize an empty list to store match information
match_info = []

# Define rewards and penalties 
offset_reward = 100  # Example reward for offset within the threshold
offset_penalty = -150  # Penalty for offset beyond the threshold
yoe_ideal_reward = 200  # Reward for ideal YOE difference
yoe_reward_ideal = 100  # Reward for YOE difference of 2-3 years
yoe_reward_good = 80  # Reward for YOE difference of 4-8 years
yoe_reward_minimal = 10  # Minimal reward for YOE difference of >8 years

# Define the offset threshold
offset_threshold = 8 

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

# Export csv for hard constraints
print('export match_1_constraints.csv')
match_scores_df.to_csv('match_1_constraints.csv')

#3.3 Reward is the overlapping by Most important Attributes
# Define the base score for an overlap
base_overlap_score = 10
# Additional rewards based on ranking in 'Most Important Attributes'
importance_weights = [3, 2, 1.5]

# Loop through the match_info list to count overlaps and adjust scores
for match in match_info:
    mentor_email = match['Mentor']
    mentee_email = match['Mentee']
    mentor_row = mentors_df.loc[mentor_email]
    mentee_row = mentees_df.loc[mentee_email]

    # Initialize important_attr_score and total overlap count
    important_attr_score = 0
    total_overlap_count = 0

    # List of attributes to check for overlaps
    attributes = ['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']

    # Iterate over each attribute to check for overlaps and their importance
    for attr in attributes:
        # Calculate the overlap
        mentor_values = set(mentor_row[attr])
        mentee_values = set(mentee_row[attr])
        overlap = mentor_values.intersection(mentee_values)
        overlap_count = len(overlap)
        
        # Update the total overlap count
        total_overlap_count += overlap_count
        
        # Initialize individual importance weights
        mentor_importance_weight = 0
        mentee_importance_weight = 0

        # Calculate the score for overlaps, considering importance
        if overlap:
            # Initialize the importance_weight
            importance_weight = 0
            # Ignore if the mentor's most important attribute is "No Preference"
            if "No Preference" not in mentor_row['Most Important Attribute']:
                # Check if this attribute is marked as important by the mentor and add its weight
                if attr in mentor_row['Most Important Attribute']:
                    mentor_importance_index = mentor_row['Most Important Attribute'].index(attr)
                    mentor_importance_weight = importance_weights[mentor_importance_index]
            # Ignore if the mentee's most important attribute is "No Preference"
            if "No Preference" not in mentee_row['Most Important Attribute']:
                # Check if this attribute is marked as important by the mentee and add its weight
                if attr in mentee_row['Most Important Attribute']:
                    mentee_importance_index = mentee_row['Most Important Attribute'].index(attr)
                    mentee_importance_weight = importance_weights[mentee_importance_index]
                
            # Sum the importance weights from mentor and mentee
            total_importance_weight = mentor_importance_weight + mentee_importance_weight
            
            # Apply the combined importance weight to the base score for each overlap
            attr_score = overlap_count * base_overlap_score * total_importance_weight  # Multiplicative effect

            # Add the attribute score to the total important_attr_score
            important_attr_score += attr_score

    # Update the match entry with the total_overlap_count and important_attr_score
    match.update({
        'Counts of Overlap': total_overlap_count,
        'Important Attributes Score': important_attr_score,
        # Update the total match score to include the important_attr_score
        'Match Score': match['Match Score'] + important_attr_score
    })

# Convert the updated match information into a DataFrame
match_scores_df = pd.DataFrame(match_info)
# Reorder columns to ensure 'Match Score' is the last column
final_columns_order = ['Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 'YOE Difference', 
                       'YOE Score', 'Counts of Overlap', 'Important Attributes Score',
                       'Match Score']
match_scores_df = match_scores_df[final_columns_order]

# Export csv
print('export match_2_overlaps.csv')
match_scores_df.to_csv('match_2_overlaps.csv')

#3.4 Reward people who write Open Answer
# Assuming 'match_info' is a list of dictionaries containing match details
# Define the reward for providing an open answer
open_answer_reward = 20

# Loop through each match to update the score based on the provision of an open answer
for match in match_info:
    mentor_email = match['Mentor']
    mentee_email = match['Mentee']

    # Retrieve the mentor and mentee rows from their respective DataFrames
    mentor_row = mentors_df.loc[mentor_email]
    mentee_row = mentees_df.loc[mentee_email]

    # Initialize Open Answer Score for this match
    match['Open Answer Score'] = 0

    # Check if an open answer was provided by the mentor or mentee
    if mentor_row['Open Answer'] or mentee_row['Open Answer']:
        # Add the open answer reward to the open answer score
        match['Open Answer Score'] += open_answer_reward

    # Update the Match Score by adding the Open Answer Score to the existing Match Score
    match['Match Score'] += match['Open Answer Score']

# Convert the updated match_info list into a DataFrame for further analysis
match_scores_df = pd.DataFrame(match_info)

# Reorder columns to ensure 'Match Score' is the last column
final_columns_order = ['Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 'YOE Difference', 
                       'YOE Score', 'Counts of Overlap', 'Important Attributes Score', 
                       'Open Answer Score', 'Match Score']
match_scores_df = match_scores_df[final_columns_order]

# Export csv
print('export match_3_openanswer.csv')
match_scores_df.to_csv('match_3_openanswer.csv')

#3.5 Rewarding Mentees Who Applied to Be Mentors
# Define the reward for mentees who have also applied to be mentors
mentee_mentor_application_reward = 15  # Example reward value

# Loop through each match to update the score based on mentee's application to be a mentor
for match in match_info:
    mentee_email = match['Mentee']

    # Check if the mentee has applied to be a mentor
    applied_to_mentor = mentees_df.loc[mentee_email, 'Apply mentor']
    

    # Initialize Applied to Mentor Score for this match
    match['Applied to Mentor Score'] = 0

    # If the mentee has applied to be a mentor, add the reward to the match score
    if applied_to_mentor == 'Yes':
        match['Match Score'] += mentee_mentor_application_reward
        match['Applied to Mentor Score'] += mentee_mentor_application_reward

# Convert the updated match_info list into a DataFrame for further analysis
match_scores_df = pd.DataFrame(match_info)

# Ensure 'Match Score' is the last column by setting the column order
final_columns_order = ['Mentor', 'Mentee', 'Offset Difference', 'Offset Score', 'YOE Difference', 
                       'YOE Score', 'Counts of Overlap', 'Important Attributes Score', 
                       'Open Answer Score', 'Applied to Mentor Score', 'Match Score']
match_scores_df = match_scores_df[final_columns_order]
# Export csv 
print('export match_4_applymentor.csv')
match_scores_df.to_csv('match_4_applymentor.csv')

#Step 4: Selecting Highest 2 Matched Mentees for Each Mentor
#1. Sort the DataFrame by 'Mentor' and 'Match Score' in descending order
sorted_matches = match_scores_df.sort_values(by=['Mentor', 'Match Score'], ascending=[True, False])

#2. Group by 'Mentor' and take the first 2 matches for each mentor
top_2_matches = sorted_matches.groupby('Mentor').head(2)

# Export csv for hard constraints
print('export match_5_top2.csv')
top_2_matches.to_csv('match_5_top2.csv')

#3. Leave only email and Match score
final_columns_order = ['Mentor', 'Mentee', 'Match Score']
match_scores_df = top_2_matches[final_columns_order]

# Export csv for hard constraints
print('export match_6_final.csv')
match_scores_df.to_csv('match_6_final.csv')

#Step 5: Exam the matching result 
#1. Statistical Analysis of Match Scores
# - check matchcurrent_analysis.py
# - previous one, check matchprevious_analysis.py

#2. Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()

print(f"Number of mentors who got matched: {unique_mentors_matched}")

