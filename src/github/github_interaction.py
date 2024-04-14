# github_interaction.py
from github import Github
import os
import sys

def get_pull_request_details():
    """
    Fetches and returns details for a specified pull request using environment variables.
    """
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')

    if not all([token, repo_name, pr_number]):
        sys.exit('Required environment variables are missing. Ensure GITHUB_TOKEN, GITHUB_REPOSITORY, and PR_NUMBER are set.')

    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    return pr

def main():
    pr_details = get_pull_request_details()
    print(f"Title: {pr_details.title}")
    print(f"Author: {pr_details.user.login}")
    print(f"Body: {pr_details.body}")

if __name__ == '__main__':
    main()
