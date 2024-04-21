import requests
import os
import sys
from llamaapi import LlamaAPI

def fetch_pr_diff(repo, pr_number, token):
    """Fetches the diff for a given pull request number from a repository."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch PR diff: {response.status_code} {response.text}")
        return None

REQUEST = """
Please provide a thorough and detailed review of the following code changes. 
Focus on identifying any issues with clarity, efficiency, and maintainability. 
Explain why these issues might be problematic, suggest better coding practices, 
and provide alternative solutions if applicable. Include specific examples or suggestions wherever possible.
"""

def get_prompt(diff):
    return [{
        "role": "system",
        "content": REQUEST
    }, {
        "role": "user",
        "content": f"Here are some recent code changes:\n\n```diff\n{diff}\n```"
    }]

def main():
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")
    if not repo or not pr_number or not token:
        print("Environment setup error.")
        sys.exit(1)

    diff = fetch_pr_diff(repo, pr_number, token)
    if not diff:
        print("No diff available.")
        return

    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("LLAMA_API_KEY is not set.")
        sys.exit(1)
    
    llama = LlamaAPI(api_key)
    messages = get_prompt(diff)

    api_request_json = {
        "model": "mistral-7b",
        "messages": messages,
        "max_tokens": 7000,
        "temperature": 0.5,
        "top_p": 1,
        "stream": False
    }

    response = llama.run(api_request_json)
    if response.ok:
        response_json = response.json()
        review_texts = [choice.get('message', {}).get('content', '') for choice in response_json.get('choices', []) if choice.get('message')]
        review_text = ' '.join(review_texts).strip()
        if review_text:
            with open('review_results.txt', 'w') as file:
                file.write(review_text)
            print("Review results written to review_results.txt")
        else:
            print("No review text was generated.")
    else:
        print(f"API request failed with status code {response.status_code}: {response.text}")

if __name__ == "__main__":
    main()
