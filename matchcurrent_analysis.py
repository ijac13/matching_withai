import pandas as pd #Python Data Analysis Library
import matplotlib.pyplot as plt # Visualization with Python
import numpy as np

#1. Load the data to analysis
match_scores_df = pd.read_csv('match_6_final.csv')

#2. Analysis in numpy
print('\n Analysis in numpy ---')
# Convert your list to a numpy array for efficient numerical operations
match_score_array = np.array(match_scores_df['Match Score'])

# Calculate minimum, maximum, mean, and standard deviation
min_diff = np.min(match_score_array)
max_diff = np.max(match_score_array)
mean_diff = np.mean(match_score_array)
std_diff = np.std(match_score_array)

# Print out the statistics
print(f"Minimum Score: {min_diff}")
print(f"Maximum Score: {max_diff}s")
print(f"Average (Mean) Score: {mean_diff}")
print(f"Standard Deviation of Score: {std_diff}")

# If you want to see individual data points, consider printing the array or parts of it
print("Sample of Score:", match_score_array[:10])  # Print the first 10 for a sample

#2. Count unique mentors who got matched
unique_mentors_matched = match_scores_df['Mentor'].nunique()

print(f"Number of mentors who got matched: {unique_mentors_matched}")

#2 Analysis in Visulization
print('\n Analysis in Visulization ---') 
# Create the plot
plt.figure(figsize=(10, 6)) 

# Ensure you're passing only the 'Match Score' column to plt.hist()
counts, bins, patches = plt.hist(match_scores_df['Match Score'], bins=12, edgecolor='black')

bin_centers = 0.5 * (bins[:-1] + bins[1:])
plt.xticks(bin_centers, labels=[f"{round(b, 2)}" for b in bin_centers], rotation=45)

# Label your axes
plt.title('Distribution of Match Score')
plt.xlabel('Score')
plt.ylabel('Counts')

# Show the plot
plt.show()

