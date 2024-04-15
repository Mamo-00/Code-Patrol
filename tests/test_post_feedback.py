from unittest.mock import patch
from github.post_feedback import post_comment_to_pr

def test_post_comment_to_pr():
    with patch('github.post_feedback.Github') as mock_github:
        mock_instance = mock_github.return_value
        mock_repo = mock_instance.get_repo.return_value
        mock_pr = mock_repo.get_pull.return_value
        mock_pr.create_issue_comment.return_value = None  # Simulate success

        with patch('github.post_feedback.os.getenv', side_effect=lambda k: {'GITHUB_TOKEN': 'fake-token', 'GITHUB_REPOSITORY': 'repo/name', 'PR_NUMBER': '123'}.get(k, None)):
            post_comment_to_pr("Test comment")
            mock_pr.create_issue_comment.assert_called_once_with("Test comment")
