import json

# File paths
submissions_file_path = 'datascience_submissions'  # Adjust as necessary
comments_file_path = 'datascience_comments'  # Adjust as necessary

# Load comments data first, to categorize by submission ID
comments_by_submission = {}
with open(comments_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            comment = json.loads(line.strip())
            link_id = comment['link_id'][3:]  # Remove 't3_' prefix
            if link_id not in comments_by_submission:
                comments_by_submission[link_id] = []
            comments_by_submission[link_id].append(comment['body'])
        except json.JSONDecodeError as e:
            continue  # Skip lines that can't be parsed

# Now read submissions and collect only those with comments
questions_and_responses = {}
with open(submissions_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            submission = json.loads(line.strip())
            submission_id = submission['id']
            if submission_id in comments_by_submission:
                # Add to questions_and_responses if this submission has comments
                questions_and_responses[submission_id] = {
                    "title": submission['title'],
                    "responses": comments_by_submission[submission_id]
                }
                if len(questions_and_responses) >= 200:
                    # Stop once we have 200 questions with responses
                    break
        except json.JSONDecodeError as e:
            continue  # Skip lines that can't be parsed

# You now have up to 200 questions with responses
# Optionally save this to a file
organized_data_file_path = 'organized_questions_with_responses'
with open(organized_data_file_path, 'w', encoding='utf-8') as file:
    json.dump(questions_and_responses, file, ensure_ascii=False, indent=4)

print(f"Collected {len(questions_and_responses)} questions with responses.")
