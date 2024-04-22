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

REQUEST = "Reply with a detailed review of the provided code changes and give code examples of specific changes. Limit suggestions to 3 high quality examples and focus on improvements for clarity, efficiency, and maintainability. If there are no issues then reply with a confirmation that the there are no issues with the code"

PERSONA = "You are an experienced software developer in a variety of programming languages and methodologies. You create efficient, scalable, and fault-tolerant solutions"

STYLE = "Format feedback concisely with bullet points"

def get_prompt(diff):
    return [{
        "role": "system",
        "content": "{}. {}. {}".format(PERSONA, STYLE, REQUEST)
    }, {
        "role": "user",
        "content": f"Please provide a detailed review of the provided code changes that I need you to analyse and give me improvements on:\n\n```diff\n{diff}\n```"
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
        "model": "codellama-34b-instruct",
        "messages": messages,
        "max_tokens": 7000,
        "temperature": 0.3,
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
