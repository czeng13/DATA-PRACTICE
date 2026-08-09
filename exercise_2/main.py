import requests
import csv
import os
import logging

logger = logging.getLogger(__name__)

page = 1
repos = []
seen_repos = set()
api_calls = 0
max_api_calls = 50
token = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

def get_data(page):
    global api_calls

    if api_calls >= max_api_calls:
        logger.info('max api calls reached')
        return None

    api_calls += 1

    response = requests.get(
        'https://api.github.com/orgs/microsoft/repos',
        headers=headers,
        params={
            'per_page': 10,
            'page': page
        }
    )
    logger.info(f'API call #{api_calls} | page {page} | status {response.status_code}')

    if response.status_code == 200:
        return response.json()

    print(response.json())
    return None


def extract_fields(data):
    for repo in data:
        
        repos.append({
            'repo_id': repo['id'],
            'repo_name': repo['name'],
            'full_name': repo['full_name'],
            'language': repo['language'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
        })
        logger.info(f"Adding distinct repo {repo['name']}")
    return repos

def dedupe_repos(repos):
    unique_repos = []
    seen_ids = set()
    
    for repo in repos:
        if repo['repo_id'] not in seen_ids:
            unique_repos.append(repo)
            seen_ids.add(repo['repo_id'])
        else:
            logger.info(f"Duplicate repo {repo['repo_name']} found and removed")
    return unique_repos

def sort_data(repos):
    filtered_repos = []
    for repo in repos:
        if repo['stars'] > 1000:
            print(repo['repo_id'], repo['stars'])
            filtered_repos.append(repo)
        
    sorted_repos = sorted(filtered_repos, key=lambda x: x['stars'], reverse=True)
    logger.info(f"Filtered and sorted {len(sorted_repos)} repos with more than 1000 stars in descending order")
    return sorted_repos

def write_to_csv(filtered_repos):
    with open('repos.csv', 'w', newline='') as csvfile:
        fieldnames = ['repo_id', 'repo_name', 'full_name', 'language', 'stars', 'forks', 'created_at', 'updated_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for repo in filtered_repos:
            writer.writerow(repo)

while True:
    repo_data = get_data(page)

    if repo_data is None:
        break

    if not repo_data:
        break

    repos = extract_fields(repo_data)
    page += 1
    
print(len(repos))

deduped_repos = dedupe_repos(repos)    
print(len(deduped_repos))
filtered_repos = sort_data(deduped_repos)
print(len(filtered_repos))
write_to_csv(filtered_repos)