import requests
from datetime import datetime, timedelta
from config import GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME

def fetch_merged_prs(days=30):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }

    since = (datetime.now() - timedelta(days=days)).isoformat()
    url = f'https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/pulls'
    params = {
        'state': 'closed',
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100,
        'since': since
    }

    response = requests.get(url, headers=headers, params=params)
    prs = response.json()

    merged_prs = [pr for pr in prs if pr['merged_at'] is not None]
    return merged_prs

if __name__ == "__main__":
    prs = fetch_merged_prs()
    print(f"Fetched {len(prs)} merged PRs from GitHub")