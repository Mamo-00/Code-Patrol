import pytest
from unittest.mock import patch, MagicMock
from analysis.code_review import get_prompt, main

def test_get_prompt():
    diff = "diff --git a/./analysis/code_review.py b/./analysis/code_review.py"
    prompt = get_prompt(diff, "developer", "detailed", False)
    # Update the expected prompt based on the actual function implementation
    expected_prompt = "**developer: Provide detailed, in-depth analysis of the code.**\n\n" \
                      "Please provide detailed, constructive feedback on the code below. Focus on improving clarity, efficiency, and maintainability. Include up to three specific examples or suggestions.\n\n" \
                      "```diff\ndiff --git a/./analysis/code_review.py b/./analysis/code_review.py\n```"
    assert prompt == expected_prompt


import pytest
from unittest.mock import patch, MagicMock
from analysis.code_review import get_prompt, main

def test_get_prompt():
    diff = "diff --git a/analysis/code_review.py b/analysis/code_review.py"
    prompt = get_prompt(diff, "developer", "detailed")
    expected_prompt = ("**developer: detailed**\n\n"
                       "Please provide detailed, constructive feedback on the code below. Focus on improving clarity, efficiency, and maintainability. Include up to three specific examples or suggestions.\n\n"
                       "```diff\ndiff --git a/analysis/code_review.py b/analysis/code_review.py\n```")
    assert prompt == expected_prompt

@patch('requests.post')
@patch('os.getenv')
def test_main(mock_getenv, mock_post):
    # Setup environment variables
    mock_getenv.side_effect = lambda var_name, default=None: {
        "LLAMA_API_KEY": "fake-key",
        "PERSONA": "developer",
        "STYLE": "detailed"
    }.get(var_name, default)

    # Prepare the mock response for requests.post to simulate the Llama API
    fake_response = {
        "choices": [
            {"text": "No issues found."}
        ]
    }
    mock_response = MagicMock()
    mock_response.json.return_value = fake_response
    mock_post.return_value = mock_response

    with patch('sys.stdin.read', return_value="fake diff"):
        result = main()
        assert result == "No issues found."



