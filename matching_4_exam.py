import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Load results from current and previous cohorts
current_results = pd.read_csv('match_3_matches.csv')
previous_results = pd.read_csv('spring2024_results.csv')

# Calculate average match scores
current_avg_score = current_results['Match Score'].mean()
previous_avg_score = previous_results['distance_score'].mean()

print(f"Average Match Score - Current Cohort: {current_avg_score}")
print(f"Average Match Score - Previous Cohort: {previous_avg_score}")

# # Perform t-test if needed
t_stat, p_value = ttest_ind(current_results['Match Score'], previous_results['distance_score'])
print(f"T-Test results -- T-statistic: {t_stat}, P-value: {p_value}")

# Visualize the score distributions
plt.hist(current_results['Match Score'], alpha=0.5, label='Current with AI')
plt.hist(previous_results['distance_score'], alpha=0.5, label='Previous')
plt.title('Distribution of Match Scores Comparison')
plt.xlabel('Match Score')
plt.ylabel('Frequency')
plt.legend()
plt.show()

#Further analysis based on surveys or other metrics could follow similar patterns
