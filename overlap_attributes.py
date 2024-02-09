import pandas as pd #Python Data Analysis Library

# Sample data for one mentor and one mentee
mentor_data = {
    'Roles': "Breaking into Product ,APM/Junior Level",
    'Industry': "B2B SaaS,No Preference",
    'Company Stage': "Public,Series D+",
    'Topics': "Breaking into Product,No Preference - general advice; meeting new people,Improve PM Skills - product sense; UX; discovery,Improve PM Skills - stakeholder management; interpersonal,Career Guidance - networking; finding new job opportunities,Career Guidance - planning career path; growth opportunities",
    'In-Person Meeting Location': "City1, City2"
}

mentee_data = {
    'Roles': "Breaking into Product ,APM/Junior Level",
    'Industry': "B2B SaaS,AI",
    'Company Stage': "Series C,Series D+,Public,Series B",
    'Topics': "Career Guidance - planning career path; growth opportunities,Career Guidance - networking; finding new job opportunities,Breaking into Product,Navigating a Transition - new job or industry",
    'In-Person Meeting Location': "City2, City3"
}

# Function to find overlaps
def find_overlaps(mentor, mentee, attribute):
    mentor_values = set(value.strip() for value in mentor[attribute].split(','))
    mentee_values = set(value.strip() for value in mentee[attribute].split(','))
    
    # Find the intersection of mentor's and mentee's values for the attribute
    overlap = mentor_values.intersection(mentee_values)
    overlap_count = len(overlap)  # Count the number of overlapping values
    
    if overlap:
        print(f"Overlap in {attribute}: {', '.join(overlap)} (Count: {overlap_count})")
    else:
        print(f"No overlap in {attribute}")

    return overlap_count  # Return the count of overlapping values

# Iterate over attributes and print overlaps
for attribute in ['Roles', 'Industry', 'Company Stage', 'Topics', 'In-Person Meeting Location']:
    find_overlaps(mentor_data, mentee_data, attribute)