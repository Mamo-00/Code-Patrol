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


@patch('analysis.code_review.openai.Completion.create')
@patch('analysis.code_review.os.getenv')
def test_main(mock_getenv, mock_create):
    # Setup environment variables
    mock_getenv.side_effect = lambda k, d=None: {
        'API_TO_USE': 'openai',
        'OPENAI_API_KEY': 'fake-key',
        'PERSONA': 'developer',
        'STYLE': 'detailed',  # Ensure this is a valid key in STYLES
        'INCLUDE_FILES': 'false'
    }.get(k, d)

    # Create a deep mock for the response to simulate the response structure of openai.Completion.create
    response_text = "No issues found."
    mock_choice = MagicMock()
    mock_choice.get.return_value = response_text

    # Properly chain mock calls
    mock_response = MagicMock()
    mock_response.get.return_value = [mock_choice]  # Simulate list from choices
    mock_create.return_value = mock_response

    with patch('sys.stdin.read', return_value=""):
        result = main()
        assert result == "No issues found."

