import pandas as pd #Python Data Analysis Library
import matplotlib.pyplot as plt # Visualization with Python
import numpy as np

# Step 1: Data Preparation

# 1.1 Clean the Data
# Load the data
mentors_df = pd.read_csv('Mentor_Submissions.csv')
mentees_df = pd.read_csv('Mentee_Submissions.csv')
no_reply_df = pd.read_csv('No-Reply_list.csv')  

## Check existing columns
# print('Check existing columns')
# print("Mentor DataFrame columns:", mentors_df.columns)
# print("Mentee DataFrame columns:", mentees_df.columns)
# print("No-Reply DataFrame columns:", no_reply_df.columns)

# Select only the necessary columns
mentors_df = mentors_df[['Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Most Important Attribute', 
                         'Open Answer', 'Cohort', 'Full Name', 'Test content', 'Avg Year of YOE']]
mentees_df = mentees_df[['Email', 'Participation Commitment', 'Offset', 'In-Person Meeting Location', 
                         'Roles', 'Industry', 'Company Stage', 'Topics', 'Most Important Attribute', 
                         'Open Answer', 'Cohort', 'Full Name', 'Test content', 'Avg Year of YOE', 'Apply mentor']]
no_reply_df = no_reply_df[['Email']]

# Strip leading/trailing spaces and convert to lower case for consistency
mentors_df['Email'] = mentors_df['Email'].str.strip().str.lower()
mentees_df['Email'] = mentees_df['Email'].str.strip().str.lower()
no_reply_df['Email'] = no_reply_df['Email'].str.strip().str.lower()  

# Check the necessary columns
print('\nCheck the necessary columns')
print("Mentor DataFrame columns:", mentors_df.columns)
print("Mentee DataFrame columns:", mentees_df.columns)
print("No-Reply DataFrame columns:", no_reply_df.columns)

# Count current cohort submissions
mentors_df = mentors_df[(mentors_df['Cohort'] == 'Fall 2023')]
mentees_df = mentees_df[(mentees_df['Cohort'] == 'Fall 2023')]

# Print current cohort submissions
print('Current cohort total submissions ---')
print(f"Mentor submissions: {len(mentors_df)}")
print(f"Mentee submissions: {len(mentees_df)}")

# Filter 1. exclude test content
# Filter 2. include only those who have committed
# Filter 3. include only current cohort
# Fitler 4. exclude from no-reply list
mentors_df = mentors_df[(mentors_df['Test content'] != 'true') 
                        & (mentors_df['Participation Commitment'] == 'Yes')
                        & (mentors_df['Cohort'] == 'Fall 2023')
                        & ~mentors_df['Email'].isin(no_reply_df['Email'])]
mentees_df = mentees_df[(mentees_df['Test content'] != 'true') 
                        & (mentees_df['Participation Commitment'] == 'Yes')
                        & (mentees_df['Cohort'] == 'Fall 2023')
                        & ~mentees_df['Email'].isin(no_reply_df['Email'])]

# # debug: Print the first 5 rows of the mentors and mentees DataFrames to verify the cleaning
# # print("Filter by current cohort")
# # print("Mentors:", mentors_df.head())
# # print("Mentees:", mentees_df.head())


# Print filtering results
print('\nCompare filtering results ---')
print(f"Mentor submissions after filtering: {len(mentors_df)}")
print(f"Mentee submissions after filtering: {len(mentees_df)}")

# Remove duplicates on 'Email' field and keep='first' to keep the first occurrence.
mentors_df = mentors_df.drop_duplicates(subset=['Email'], keep='first')
mentees_df = mentees_df.drop_duplicates(subset=['Email'], keep='first')

# # debug
# # print('Remove duplications')
# # print("Mentors columns:", mentors_df.info())
# # print("Mentees columns:", mentees_df.info())
# # print("Mentors:", mentors_df.head())
# # print("Mentees:", mentees_df.head())

# Print removing duplication results
print('\nCompre removing duplications --- ')
print(f"Mentor submissions after removing duplicates: {len(mentors_df)}")
print(f"Mentee submissions after removing duplicates: {len(mentees_df)}")

# # debug: Manually check if an email expected to be in no_reply_df is present in mentors_df
# # test_email = 'example@gmail.com'  
# # print("test email in mentors:", test_email in mentors_df['Email'].values) 
# # print("test email in no-reply:", test_email in no_reply_df['Email'].values) 

# #1.2 Structure the Data

# Set 'Email' as the index
mentors_df.set_index('Email', inplace=True)
mentees_df.set_index('Email', inplace=True)

# Drop unnecessary columns
mentors_df.drop(['Participation Commitment', 'Test content'], axis=1, inplace=True)
mentees_df.drop(['Participation Commitment', 'Test content'], axis=1, inplace=True)

# Convert 'Open Answer' to a boolean column
mentors_df['Open Answer'] = mentors_df['Open Answer'].apply(lambda x: False if pd.isnull(x) else True)
mentees_df['Open Answer'] = mentees_df['Open Answer'].apply(lambda x: False if pd.isnull(x) else True)

# At this point, other columns are retained as is, with the following notes:
# - 'Offset' is already a float and will be used for calculations as described.
# - 'In-Person Meeting Location', 'Roles', 'Industry', 'Company Stage', 'Topics':
#   These are lists of texts and will be used for matching based on text comparison or mapping.
# - 'Most Important Attribute' contains column names and will guide the weighting in the matching algorithm.
# - 'Avg Year of YOE' is a float and will be used for experience-based matching.

# Review the updated DataFrame structure
print('\nReview the updated DataFrame structure')
print(mentors_df.info())
print(mentees_df.info())

#2. Decide Weighting System
#2.1 Decide Weighting System
# - Penalty System: This system intuitively mimics a "deduction for incompatibility" and can be easier to conceptualize when you're more focused on filtering out incompatible matches.
# - Rewarding System: This approach is intuitive when you want to "reward" compatibility and can make it easier to assign value to each matching criterion based on its importance.
# - Combining System [use this one]: This hybrid approach allows for a more nuanced scoring system that can reward compatibility while also penalizing incompatibilities, giving you a balanced view of each potential match.

#2.2 Analysis Offset to decide a threshold for maximum allowed difference
# - use offset_threshold.py to make the decision

# Compare the Offset values for each mentor-mentee pair
# offset_differences = []

# for mentor_index, mentor_row in mentors_df.iterrows():
#     mentor_offset = mentor_row['Offset']
#     for mentee_index, mentee_row in mentees_df.iterrows():
#         mentee_offset = mentee_row['Offset']
#         offset_difference = abs(mentor_offset - mentee_offset)
#         offset_differences.append(offset_difference)
# debug: see offset_differences
# print('offset_differences:', offset_differences)

#2.3 Set offset_difference threshold + match_scores
#2.4 Add Avg of YOE, this is also the  Hard Constraints

# Initialize an empty DataFrame to store match scores
match_scores = []

# Define your reward and penalty values
offset_reward = 100  # Points to add for a match within the threshold
offset_penalty = -150  # Points to subtract for a match exceeding the threshold
offset_threshold = 9 # Set the offset threshold

yoe_reward_ideal = 100  # Reward for YOE difference of 2-3 years
yoe_reward_good = 80  # Reward for YOE difference of 4-8 years
yoe_reward_minimal = 10  # Minimal reward for YOE difference of >8 years

base_overlap_score = 10
importance_scores = {1: 3, 2: 2, 3: 1.5} #Define scores based on ranking in the Most Important Attributes; Max 3

for mentor_email, mentor_row in mentors_df.iterrows():
    mentor_offset = mentor_row['Offset']
    mentor_yoe = mentor_row['Avg Year of YOE']
    mentor_important_attrs = mentor_row['Most Important Attribute'].split(', ')

    for mentee_email, mentee_row in mentees_df.iterrows():
        mentee_offset = mentee_row['Offset']
        mentee_yoe = mentee_row['Avg Year of YOE']
        mentee_important_attrs = mentee_row['Most Important Attribute'].split(', ')

        # Calculate differences
        offset_difference = abs(mentor_offset - mentee_offset)
        yoe_difference = mentor_yoe - mentee_yoe
        
         # Initialize match score
        match_score = 0
        offset_score = 0
        yoe_scroe = 0
        important_attr_score = 0
        
        # List of attributes to check for overlap
        check_attrs = ['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']

        # Apply rewards or penalties based on the offset difference
        if offset_difference <= offset_threshold:
            offset_score = offset_reward
        else:
            offset_score = offset_penalty
        match_score += offset_score

        # Apply rewards or penalties based on YOE difference, exclude if mentor's YOE <= mentee's YOE
        if mentor_yoe <= mentee_yoe:
            continue  # Skip this match
        elif 2 <= yoe_difference <= 3:
            yoe_score = yoe_reward_ideal
        elif 4 <= yoe_difference <= 8:
            yoe_score = yoe_reward_good
        elif yoe_difference > 8:
            yoe_score = yoe_reward_minimal
        match_score += yoe_score
        
        # Check for overlaps and update the score
        for attr in check_attrs:
            if mentor_row[attr] == mentee_row[attr]:  # Check for overlap
                important_attr_score += base_overlap_score  # Add base score for overlap

                # Check if the attribute is in the mentor's important attributes list and add additional score
                if attr in mentor_important_attrs:
                    rank = mentor_important_attrs.index(attr) + 1  # Get the rank (1-based index)
                    important_attr_score += importance_scores.get(rank, 0)  # Add score based on rank

                # Check if the attribute is in the mentee's important attributes list and add additional score
                if attr in mentee_important_attrs:
                    rank = mentee_important_attrs.index(attr) + 1  # Get the rank (1-based index)
                    important_attr_score += importance_scores.get(rank, 0)  # Add score based on rank
        match_score += important_attr_score

        # Append the match information to the DataFrame
        match_scores.append({
            'Mentor': mentor_email,
            'Mentee': mentee_email,
            'Offset Difference': offset_difference,
            'Offset Score': offset_score,
            'YOE Difference': yoe_difference,
            'YOE Score': yoe_score,
            'Important Attributes Score': important_attr_score,
            'Match Score': match_score
        })

# Convert the list of dictionaries into a DataFrame
match_scores_df = pd.DataFrame(match_scores)
    

# Display the match scores DataFrame
print(match_scores_df)
