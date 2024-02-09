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
print(f"Mentor submissions after removing duplications: {len(mentors_df)}")
print(f"Mentee submissions after removing duplications: {len(mentees_df)}")

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

# Compare the Offset values for each mentor-mentee pair
offset_differences = []

for mentor_index, mentor_row in mentors_df.iterrows():
    mentor_offset = mentor_row['Offset']
    for mentee_index, mentee_row in mentees_df.iterrows():
        mentee_offset = mentee_row['Offset']
        offset_difference = abs(mentor_offset - mentee_offset)
        offset_differences.append(offset_difference)
# debug: see offset_differences
# print('offset_differences:', offset_differences)


# print('\n Offset Analysis in Visulization ---') 
# # Create the plot
# plt.figure(figsize=(10, 6))  # Adjusts the size of your plot
# counts, bins, patches = plt.hist(offset_differences, bins=12, edgecolor='black')

# #calculate percentage
# total_counts = sum(counts)
# percentages = [(count / total_counts) * 100 for count in counts]
# # print('total_counts: ', total_counts)
# # print('percentages:', percentages)

# # Set x-ticks to be the bin centers for better readability
# bin_centers = 0.5 * (bins[:-1] + bins[1:])
# plt.xticks(bin_centers, labels=[f"{round(b, 2)}" for b in bin_centers], rotation=45)

# # Label your axes
# plt.title('Distribution of Offset Differences')
# plt.xlabel('Time Difference (hours)')
# # plt.ylabel('Frequency') #the number of data points that fall within each bin of the histogram. 
# # plt.ylabel('Counts') #show the count of values in each bin
# plt.ylabel('Percentage (%)')

# # Show the plot
# plt.show()


print('\n Offset Analysis in numpy ---')
# Convert your list to a numpy array for efficient numerical operations
offset_diff_array = np.array(offset_differences)

# Calculate minimum, maximum, mean, and standard deviation
min_diff = np.min(offset_diff_array)
max_diff = np.max(offset_diff_array)
mean_diff = np.mean(offset_diff_array)
std_diff = np.std(offset_diff_array)

# Print out the statistics
print(f"Minimum Offset Difference: {min_diff} hours")
print(f"Maximum Offset Difference: {max_diff} hours")
print(f"Average (Mean) Offset Difference: {mean_diff} hours")
print(f"Standard Deviation of Offset Differences: {std_diff} hours")

# If you want to see individual data points, consider printing the array or parts of it
print("Sample of Offset Differences:", offset_diff_array[:10])  # Print the first 10 for a sample

