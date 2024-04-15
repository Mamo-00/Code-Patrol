import pytest
from unittest.mock import patch, MagicMock
from github.github_interaction import get_pull_request_details

@patch('github.github_interaction.Github')
@patch('github.github_interaction.os.getenv')
def test_get_pull_request_details(mock_getenv, mock_github):
    # Configure the mock environment variables
    mock_getenv.side_effect = lambda k: {
        'GITHUB_TOKEN': 'fake-token',
        'GITHUB_REPOSITORY': 'repo/name',
        'PR_NUMBER': '123'
    }.get(k)

    # Setup Mock GitHub API responses
    mock_instance = mock_github.return_value
    mock_repo = mock_instance.get_repo.return_value
    mock_pr = mock_repo.get_pull.return_value
    mock_pr.title = "Fix Issue #123"
    mock_pr.user.login = "testuser"
    mock_pr.body = "This fixes a bug in our code."

    # Call the function under test
    pr_details = get_pull_request_details()

    # Assertions to verify the behavior
    assert pr_details.title == "Fix Issue #123"
    assert pr_details.user.login == "testuser"
    assert pr_details.body == "This fixes a bug in our code."
