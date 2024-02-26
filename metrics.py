import json
from datetime import datetime

def read_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue  # Skip lines that cannot be parsed
    return data

def analyze_reddit_data(submissions, comments):
    metrics = {
        'count_posts': len(submissions),
        'count_comments': len(comments),
        'unique_authors': set(),
        'submission_date_range': [float('inf'), float('-inf')],
        'comment_date_range': [float('inf'), float('-inf')]
    }
    
    for post in submissions:
        metrics['unique_authors'].add(post.get('author'))
        created_utc = post.get('created_utc')
        if created_utc is not None:
            created_utc = int(created_utc)
            metrics['submission_date_range'][0] = min(metrics['submission_date_range'][0], created_utc)
            metrics['submission_date_range'][1] = max(metrics['submission_date_range'][1], created_utc)
    
    for comment in comments:
        metrics['unique_authors'].add(comment.get('author'))
        created_utc = comment.get('created_utc')
        if created_utc is not None:
            created_utc = int(created_utc)
            metrics['comment_date_range'][0] = min(metrics['comment_date_range'][0], created_utc)
            metrics['comment_date_range'][1] = max(metrics['comment_date_range'][1], created_utc)
    
    # Convert extreme values back to None if they were not updated
    metrics['submission_date_range'] = [None if x == float('inf') or x == float('-inf') else datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') for x in metrics['submission_date_range']]
    metrics['comment_date_range'] = [None if x == float('inf') or x == float('-inf') else datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') for x in metrics['comment_date_range']]
    
    metrics['unique_authors'] = len(metrics['unique_authors'])  # Convert to count
    
    return metrics

def main():
    submissions_file = 'datascience_submissions'  
    comments_file = 'datascience_comments'  
    
    submissions = read_data(submissions_file)
    comments = read_data(comments_file)
    
    metrics = analyze_reddit_data(submissions, comments)
    
    for key, value in metrics.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
