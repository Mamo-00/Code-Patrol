import subprocess
import os
import json

def run_flake8(target_directory):
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
    # Define paths relative to the root of the repository
    repo_root = os.getenv('GITHUB_WORKSPACE', '.')  # Use GITHUB_WORKSPACE to get the root directory
    analysis_dir = os.path.join(repo_root, 'analysis')
    github_dir = os.path.join(repo_root, 'github')

    target_directory = analysis_dir
    target_files = [
        os.path.join(analysis_dir, 'code_review.py'),
        os.path.join(github_dir, 'post_feedback.py')
    ]

    flake8_issues = run_flake8(target_directory)
    pylint_issues = run_pylint(target_files)

    print("Flake8 Issues:", json.dumps(flake8_issues, indent=4))
    print("Pylint Issues:", json.dumps(pylint_issues, indent=4))

    # Optionally save the results to a JSON file
    results_file = os.path.join(repo_root, 'analysis_results.json')
    with open(results_file, 'w') as file:
        json.dump({'flake8': flake8_issues, 'pylint': pylint_issues}, file, indent=4)

if __name__ == '__main__':
    main()
