import pandas as pd #Python Data Analysis Library
import matplotlib.pyplot as plt # Visualization with Python
import numpy as np

#1. Load the data to analysis
mentors_df = pd.read_csv('mentors_offset_analysis.csv')
mentees_df = pd.read_csv('mentees_offset_analysis.csv')

#2.Analysis Offset to decide a threshold for maximum allowed difference

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


print('\n Offset Analysis in Visulization ---') 
# Create the plot
plt.figure(figsize=(10, 6))  # Adjusts the size of your plot
counts, bins, patches = plt.hist(offset_differences, bins=12, edgecolor='black')

#calculate percentage
total_counts = sum(counts)
percentages = [(count / total_counts) * 100 for count in counts]
# print('total_counts: ', total_counts)
# print('percentages:', percentages)

# Set x-ticks to be the bin centers for better readability
bin_centers = 0.5 * (bins[:-1] + bins[1:])
plt.xticks(bin_centers, labels=[f"{round(b, 2)}" for b in bin_centers], rotation=45)

# Label your axes
plt.title('Distribution of Offset Differences')
plt.xlabel('Time Difference (hours)')
# plt.ylabel('Frequency') #the number of data points that fall within each bin of the histogram. 
# plt.ylabel('Counts') #show the count of values in each bin
plt.ylabel('Percentage (%)')

# Show the plot
plt.show()


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

