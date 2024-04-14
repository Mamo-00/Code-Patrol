import os
from github import Github

def post_comment_to_pr(comment_body):
    repo_name = os.getenv('GITHUB_REPOSITORY')
    pr_number = int(os.getenv('PR_NUMBER'))
    token = os.getenv('GITHUB_TOKEN')
    
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment_body)

def main():
    comment_body = "Your automated feedback here."
    post_comment_to_pr(comment_body)

if __name__ == '__main__':
    main()
