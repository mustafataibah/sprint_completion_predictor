import requests
from config import LINEAR_API_KEY, LINEAR_TEAM_ID

def fetch_issues():
    headers = {
        'Authorization': f'Bearer {LINEAR_API_KEY}',
        'Content-Type': 'application/json',
    }

    query = """
    query {
      issues(filter: {team: {id: {eq: "%s"}}}) {
        nodes {
          id
          title
          estimate
          startedAt
          completedAt
          state {
            name
          }
        }
      }
    }
    """ % LINEAR_TEAM_ID

    response = requests.post('https://api.linear.app/graphql', json={'query': query}, headers=headers)
    return response.json()['data']['issues']['nodes']

if __name__ == "__main__":
    issues = fetch_issues()
    print(f"Fetched {len(issues)} issues from Linear")