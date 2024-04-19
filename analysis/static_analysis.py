import subprocess
import os
import sys
import json

def run_flake8(target_directory):
    """Runs flake8 on the specified directory and returns the results as a list of issues."""
    command = ['flake8', '--format=json', target_directory]
    result = subprocess.run(command, capture_output=True, text=True)
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
        command = ['pylint', '--output-format=json', file]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            try:
                issues[file] = json.loads(result.stdout)
            except json.JSONDecodeError:
                print(f"Failed to decode pylint output for {file}.")
    return issues

def main():
    # Ensure the current directory is correct, or explicitly set it if necessary
    base_dir = os.path.dirname(__file__)  # Gets the directory where this script is located
    target_directory = os.path.join(base_dir, '..')  # Adjust path as needed
    target_files = [os.path.join(base_dir, 'analysis', 'code_review.py'),
                    os.path.join(base_dir, 'GitHub', 'post_feedback.py')]

    flake8_issues = run_flake8(target_directory)
    pylint_issues = run_pylint(target_files)

    # Print results or handle them further as needed
    print("Flake8 Issues:", json.dumps(flake8_issues, indent=4))
    print("Pylint Issues:", json.dumps(pylint_issues, indent=4))

    results_file = os.path.join(base_dir, 'analysis_results.json')
    with open(results_file, 'w') as file:
        json.dump({'flake8': flake8_issues, 'pylint': pylint_issues}, file, indent=4)

if __name__ == '__main__':
    main()
