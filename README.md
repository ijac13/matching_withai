## how to use it
1. run "matching_ai5.py". this is the latest matching. 
2. it would take up to 5~10 minutes to run.
3. when it runs, look at the IDE, it will print out information. 
4. you'll get result as match_6_addmentee.csv

# Matching with AI
A simple matching algorithm for a mentorship program.

## Why Matching?
This algorithm is designed to pair mentors and mentees who apply to the mentorship program. The program is facilitated by a few volunteers to support hundreds of applications, necessitating a system to efficiently manage the matching process.

## Why Work with AI?
* Based on the rules we've set and the discussions we've had about processing the mentorship program, we understand how we want to match mentors and mentees. However, we are all product managers with limited coding experience.
* My experience with writing using AI has been incredibly fun! 🎉 Therefore, I wanted to extend this use case to coding.
* Detailed reasons are available [here](https://coda.io/d/Internal-Lennys-Mentorship-Team_do64F2X3FtE/Embracing-AI-in-Our-Mentorship-Matching-Algorithm_su7VU#_luS6h), but access is restricted to those involved in the mentorship program that inspired me.

# The Result
**Use `matching_1_score.py` and `matching_3_loop.py`**
1. `matching_1_score.py` calculates the scores between each mentor and mentee, filtering out some based on predefined rules.
2. `matching_3_loop.py` initially matches mentors to mentees ensuring that every mentor has a match. It then repeats the process to match mentors with unmatched mentees until there are no unmatched mentees left.
   - The final result ensures that each mentor is paired with 1 to X mentees, depending on the availability and matching criteria.




