# Define the base score for an overlap and the importance weights
base_overlap_score = 10
importance_weights = [3, 2, 1.5]  # Weights for 1st, 2nd, and 3rd most important attributes

# Sample data for a mentor and mentee with one overlap in 'Industry'
mentor_data = {
    'Industry': ['Software'],  # Overlapping industry
    'Most Important Attribute': ['Industry']  # 'Industry' is the mentor's 1st most important attribute
}

mentee_data = {
    'Industry': ['Software', 'Hardware'],  # Overlapping industry plus another
    'Most Important Attribute': ['Roles', 'Topics', 'Industry']  # 'Industry' is the mentee's 3rd most important attribute
}

# Check for overlap
overlap = set(mentor_data['Industry']).intersection(set(mentee_data['Industry']))
overlap_count = len(overlap)  # Count of overlapping industries

# Initialize the score for the overlap in 'Industry'
industry_score = 0

# Calculate the score if there's an overlap
if overlap:
    # Since 'Industry' is the mentor's 1st most important attribute, use the first weight (3)
    mentor_importance_weight = importance_weights[0]
    
    # Since 'Industry' is the mentee's 3rd most important attribute, use the third weight (1.5)
    mentee_importance_weight = importance_weights[2]
    
    # Sum the importance weights from mentor and mentee
    total_importance_weight = mentor_importance_weight + mentee_importance_weight
    
    # Calculate the score for the overlap in 'Industry'
    industry_score = overlap_count * base_overlap_score * total_importance_weight

# Output the calculated industry score for validation
print(f"Industry Score: {industry_score}")
