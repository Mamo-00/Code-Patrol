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
