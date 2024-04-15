import os
import sys
import openai
from src.utils.common_utils import (extract_filenames_from_diff_text)
from utils.settings import API_KEY_NAMES, MODEL, TEMPERATURE, MAX_TOKENS, STYLES, PERSONAS, REQUEST


# Load styles and personas from settings
from utils.settings import STYLES, PERSONAS, REQUEST

# Generate prompt for LLM
def get_prompt(diff, persona, style):
    style_description = STYLES.get(style, "Default style description.")
    prompt = f"**{persona}: {style_description}**\n\n{REQUEST}\n\n```diff\n{diff}\n```"
    return prompt


# Main execution function
def main():
    api_to_use = os.getenv("API_TO_USE", "openai")
    persona = PERSONAS.get(os.getenv("PERSONA", "developer"))
    style = STYLES.get(os.getenv("STYLE", "detailed"))
    include_files = os.getenv("INCLUDE_FILES", "false").lower() == "true"

    api_key = os.getenv(API_KEY_NAMES[api_to_use])
    if not api_key:
        return "API key for {} is not set.".format(api_to_use)

    diff = sys.stdin.read()
    filenames = extract_filenames_from_diff_text(diff) if include_files else []
    prompt = get_prompt(diff, persona, style, include_files, filenames)

    try:
        response = openai.Completion.create(
            engine=MODEL, prompt=prompt, max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE, stop=None, api_key=api_key
        )
        review_text = response.get("choices")[0].get("text", "").strip()
        return review_text  
    except Exception as e:
        return f"Failed to generate review due to an error: {e}"

# If __name__ == "__main__":, call the function and print its output
if __name__ == "__main__":
    print(main())

