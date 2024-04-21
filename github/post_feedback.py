import os
from github import Github

def post_comment_to_pr(comment_body, repo_name, pr_number, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))  # Ensure pr_number is an integer
    pr.create_issue_comment(comment_body)

def main():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = os.getenv('PR_NUMBER')
    if not all([token, repo_name, pr_number]):
        print("Missing environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY, or PR_NUMBER.")
        return

    with open('review_results.txt', 'r') as file:
        review_text = file.read().strip()

    if review_text:
        post_comment_to_pr(review_text, repo_name, pr_number, token)
        print("Review comment posted successfully.")
    else:
        print("Review text is empty, no comment posted.")

if __name__ == '__main__':
    main()
