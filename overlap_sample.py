import pandas as pd #Python Data Analysis Library
# Assume base_overlap_score is 10
base_overlap_score = 10

# importance_weights is a list [3, 2, 1.5] representing the weights for 1st, 2nd, and 3rd most important attributes
importance_weights = [3, 2, 1.5]

# Sample data for mentor and mentee
mentor_row = {'Company Stage': ['Series D+'], 'Most Important Attribute': ['Company Stage']}
mentee_row = {'Company Stage': ['Series C', 'Series D+', 'Public', 'Series B']}

# Calculate overlap
overlap = set(mentor_row['Company Stage']).intersection(set(mentee_row['Company Stage']))
overlap_count = len(overlap)

# Initialize score for 'Company Stage' attribute
company_stage_score = 0

# Check for overlap and if 'Company Stage' is marked as important
if overlap and 'Company Stage' in mentor_row['Most Important Attribute']:
    # Since 'Company Stage' is the first and only item in 'Most Important Attribute', use the first weight
    importance_weight = importance_weights[0]  # 3 for the 1st important attribute
    company_stage_score = overlap_count * (base_overlap_score * importance_weight)  # Should be 30 for 1 overlap

print(f"Company Stage Score: {company_stage_score}")
