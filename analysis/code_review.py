import sys
import os
from llamaapi import LlamaAPI

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
if not LLAMA_API_KEY:
    print("LLAMA_API_KEY is not set.")
    sys.exit(1)

llama = LlamaAPI(LLAMA_API_KEY)


MODEL = "mistral-7b"
TEMPERATURE = 0.5  # Try varying this to see different outputs
MAX_TOKENS = 7000
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
    diff = sys.stdin.read()
    messages = get_prompt(diff)

    api_request_json = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "top_p": 1,
        "stream": False
    }

    try:
        response = llama.run(api_request_json)
        if response.ok:
            response_json = response.json()
            print("API Response:", response_json)  # Print the full API response
            # Adjust how you extract the review text:
            choices = response_json.get('choices', [])
            review_texts = [choice.get('message', {}).get('content', '') for choice in choices if choice.get('message')]
            review_text = ' '.join(review_texts).strip()
            if review_text:
                with open('review_results.txt', 'w') as file:
                    file.write(review_text)
                print("Review results written to review_results.txt")
            else:
                print("No review text was generated.")
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to generate review due to an error: {e}")

if __name__ == "__main__":
    main()
