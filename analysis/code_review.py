import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from settings import API_KEY_NAMES, MODEL, TEMPERATURE, MAX_TOKENS, STYLES, PERSONAS, REQUEST

def get_prompt(diff, persona, style):
    style_description = STYLES.get(style, "detailed")
    prompt = f"**{persona}: {style_description}**\n\n{REQUEST}\n\n```diff\n{diff}\n```"
    return prompt

def main():
    api_key = os.getenv("LLAMA_API_KEY")
    persona = PERSONAS.get(os.getenv("PERSONA", "developer"))
    style = STYLES.get(os.getenv("STYLE", "detailed"))
    diff = sys.stdin.read()
    prompt = get_prompt(diff, persona, style)

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }

    try:
        response = requests.post('https://api.llama-api.com/v1/completions', json=data, headers=headers)
        response_json = response.json()
        review_text = response_json.get('choices', [{}])[0].get('text', '').strip()

        # Write to a file
        with open('review_results.txt', 'w') as file:
            file.write(review_text)

        print(review_text)
    except Exception as e:
        print(f"Failed to generate review due to an error: {e}")

if __name__ == "__main__":
    main()
