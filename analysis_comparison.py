import pandas as pd
import matplotlib.pyplot as plt

# Load the match results from two CSV files
match_results_1 = pd.read_csv('Coda-Doc-Sync-Matched-List.csv')
match_results_2 = pd.read_csv('match_5_matches.csv')

# Define names for the matches
match_name_1 = 'Coda Spring 2025Matches'
match_name_2 = 'Spring 2025Matches'

# Calculate descriptive statistics for each match result
mean_score_1 = match_results_1['Match Score'].mean()
std_score_1 = match_results_1['Match Score'].std()

mean_score_2 = match_results_2['Match Score'].mean()
std_score_2 = match_results_2['Match Score'].std()

print(f"{match_name_1} - Mean: {mean_score_1}, Std Dev: {std_score_1}")
print(f"{match_name_2} - Mean: {mean_score_2}, Std Dev: {std_score_2}")

# Plot the distributions of match scores
plt.figure(figsize=(12, 6))
plt.hist(match_results_1['Match Score'], bins=20, alpha=0.5, label=match_name_1, edgecolor='black')
plt.hist(match_results_2['Match Score'], bins=20, alpha=0.5, label=match_name_2, edgecolor='black')

# Add titles and labels
plt.title('Comparison of Match Scores')
plt.xlabel('Match Score')
plt.ylabel('Frequency')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

# Box plot for visual comparison
plt.figure(figsize=(8, 4))
plt.boxplot([match_results_1['Match Score'], match_results_2['Match Score']], labels=[match_name_1, match_name_2])
plt.title('Box Plot of Match Scores')
plt.ylabel('Match Score')
plt.grid(True)
plt.show()