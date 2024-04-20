import requests  # Use requests to handle HTTP requests to the Llama API
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from settings import API_KEY_NAMES, MODEL, TEMPERATURE, MAX_TOKENS, STYLES, PERSONAS, REQUEST


def get_prompt(diff, persona, style):
    style_description = STYLES.get(style, "detailed")
    prompt = f"**{persona}: {style_description}**\n\n{REQUEST}\n\n```diff\n{diff}\n```"
    return prompt

def main():
    api_to_use = os.getenv("API_KEY_NAMES", "llama")
    persona = PERSONAS.get(os.getenv("PERSONA", "developer"))
    style = STYLES.get(os.getenv("STYLE", "detailed"))

    api_key = os.getenv(API_KEY_NAMES[api_to_use])
    if not api_key:
        return "API key for {} is not set.".format(api_to_use)

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
        return review_text
    except Exception as e:
        return f"Failed to generate review due to an error: {e}"

if __name__ == "__main__":
    print(main())
