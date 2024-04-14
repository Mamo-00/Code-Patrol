import subprocess
import sys
import json

def run_flake8(target_directory):
    """Runs flake8 on the specified directory and returns the results as a list of issues."""
    result = subprocess.run(
        ['flake8', '--format=json', target_directory],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        try:
            issues = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Failed to decode flake8 output.")
            return None
        return issues
    return {}

def run_pylint(target_files):
    """Runs pylint on the specified files and returns the results as a list of issues."""
    issues = {}
    for file in target_files:
        result = subprocess.run(
            ['pylint', '--output-format=json', file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            try:
                issues[file] = json.loads(result.stdout)
            except json.JSONDecodeError:
                print(f"Failed to decode pylint output for {file}.")
    return issues

def main():
    flake8_issues = run_flake8('src/')
    pylint_issues = run_pylint(['src/analysis/code_review.py', 'src/GitHub/post_feedback.py'])

    # Print results or handle them further as needed
    print("Flake8 Issues:", json.dumps(flake8_issues, indent=4))
    print("Pylint Issues:", json.dumps(pylint_issues, indent=4))

    with open('analysis_results.json', 'w') as file:
        json.dump({'flake8': flake8_issues, 'pylint': pylint_issues}, file, indent=4)

if __name__ == '__main__':
    main()
