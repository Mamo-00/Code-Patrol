import requests

def analyze_code_with_openai(code_snippet):
    api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }
    data = {
        "prompt": code_snippet,
        "temperature": 0.5,
        "max_tokens": 100,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    response = requests.post(api_url, headers=headers, json=data).json()
    return response.get("choices", [{}])[0].get("text", "")

# Example usage
code_snippet = "for i in range(10): print(i)"
feedback = analyze_code_with_openai(code_snippet)
print(feedback)
