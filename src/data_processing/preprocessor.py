import pandas as pd
from datetime import datetime

def preprocess_data(issues, prs):
    # Convert issues to DataFrame
    issues_df = pd.DataFrame(issues)
    issues_df['startedAt'] = pd.to_datetime(issues_df['startedAt'])
    issues_df['completedAt'] = pd.to_datetime(issues_df['completedAt'])
    
    # Convert PRs to DataFrame
    prs_df = pd.DataFrame(prs)
    prs_df['created_at'] = pd.to_datetime(prs_df['created_at'])
    prs_df['merged_at'] = pd.to_datetime(prs_df['merged_at'])
    
    # Merge issues and PRs (assuming PR title contains issue ID)
    merged_df = pd.merge(issues_df, prs_df, left_on='id', right_on='title', how='inner')
    
    # Calculate completion time in days
    merged_df['completion_time'] = (merged_df['merged_at'] - merged_df['startedAt']).dt.total_seconds() / (24 * 3600)
    
    # Extract features
    features_df = merged_df[['estimate', 'completion_time']]
    features_df['day_of_week'] = merged_df['startedAt'].dt.dayofweek
    
    return features_df

if __name__ == "__main__":
    # For testing purposes
    from src.data_collection.linear_api import fetch_issues
    from src.data_collection.github_api import fetch_merged_prs
    
    issues = fetch_issues()
    prs = fetch_merged_prs()
    processed_data = preprocess_data(issues, prs)
    print(processed_data.head())