import requests  # Use requests to handle HTTP requests to the Llama API
import sys
import os

# API keys
API_KEY_NAMES = {
    "llama": "LLAMA_API_KEY",  # Name of the environment variable where the Llama API key is stored
    "github": "GITHUB_TOKEN"
}

# Model and API usage settings
MODEL = "llama-2"  # Assuming you're using a model like llama-2, adjust based on actual available models
TEMPERATURE = 0.1
MAX_TOKENS = 7000

# Request templates and styles for LLM prompts
REQUEST = "Please provide detailed, constructive feedback on the code below. Focus on improving clarity, efficiency, and maintainability. Include up to three specific examples or suggestions."

STYLES = {
    "concise": "Provide feedback concisely with bullet points.",
    "detailed": "Provide detailed, in-depth analysis of the code.",
    "educational": "Explain the code and its potential issues like teaching a student.",
}

PERSONAS = {
    "developer": "Experienced developer offering practical advice.",
    "educator": "Educator focusing on teaching best practices and principles.",
}



def get_prompt(diff, persona, style):
    style_description = STYLES.get(style, "Detailed analysis")
    prompt = f"**{persona}: {style_description}**\n\n{REQUEST}\n\n```diff\n{diff}\n```"
    return prompt

def main():
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("LLAMA_API_KEY is not set.")
        return

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
        if response.status_code == 200:
            response_json = response.json()
            review_text = response_json.get('choices', [{}])[0].get('text', '').strip()
            with open('review_results.txt', 'w') as file:
                file.write(review_text)
            print("Review results written to review_results.txt")
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to generate review due to an error: {e}")

if __name__ == "__main__":
    main()
