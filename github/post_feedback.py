import os
import sys

from github import Github

def post_comment_to_pr(comment_body):
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number_str = os.getenv('PR_NUMBER')
    token = os.getenv('GITHUB_TOKEN')

    if not pr_number_str:
        raise ValueError("PR_NUMBER environment variable is missing or invalid.")

    pr_number = int(pr_number_str)  # Safely convert to int after checking

    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment_body)


def main(comment_body):
    post_comment_to_pr(comment_body)

if __name__ == '__main__':
    # Expects the review text as the first command line argument
    comment_body = sys.argv[1] if len(sys.argv) > 1 else "Default comment"
    main(comment_body)

