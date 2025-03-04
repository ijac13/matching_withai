import pandas as pd  # Python Data Analysis Library
import matplotlib.pyplot as plt  # Visualization with Python

# 1. Load the data to analysis
match_scores_df = pd.read_csv('match_5_matches.csv')

# 2. Analysis in Visualization
print('\\n Analysis in Visualization ---')
# Create the plot
plt.figure(figsize=(10, 6))  # Adjusts the size of your plot

# Ensure you're passing only the 'Match Score' column to plt.hist()
counts, bins, patches = plt.hist(match_scores_df['Match Score'], bins=12, edgecolor='black')

# Calculate bin centers to use as xticks
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# Update xticks to use bin centers
plt.xticks(bin_centers, labels=[f"{round(b, 2)}" for b in bin_centers], rotation=45)

# Label your axes
plt.title('Distribution of Match Scores')
plt.xlabel('Match Score')
plt.ylabel('Counts')

# Show the plot
plt.show()
