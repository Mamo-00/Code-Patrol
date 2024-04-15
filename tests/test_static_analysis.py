import pytest
from unittest.mock import patch, MagicMock
from analysis.static_analysis import run_flake8, run_pylint

def test_run_flake8():
    with patch('analysis.static_analysis.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout='{}')
        issues = run_flake8('./')
        assert issues == {}

def test_run_pylint():
    with patch('analysis.static_analysis.subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout='[]')
        issues = run_pylint(['analysis.code_review'])
        assert issues == {}
