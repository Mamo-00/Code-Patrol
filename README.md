
# Code-Patrol
This project is about building an application that uses AI to do code review and give feedback. The idea is to make a tool that spots mistakes, suggests better ways to write code, or even helps explain tough parts of the code. It will use LLMs to understand the code and to offer useful advice.

## AI-Powered Code Review GitHub Action

## Introduction
The AI-Powered Code Review GitHub Action is an innovative tool designed to automate the code review process on GitHub repositories. Utilizing advanced Large Language Models (LLMs) such as Llama, this action provides real-time feedback on pull requests, identifying errors, suggesting optimizations, and explaining complex parts of the code. This tool aims to enhance coding standards, reduce human review workload, and accelerate the learning curve for developers.

### Features
- **Automated Code Analysis:** Scans code in pull requests to automatically detect and report errors.
- **Error Detection:** Pinpoints syntax errors, logical mistakes, and potential security vulnerabilities.
- **Optimization Suggestions:** Offers recommendations to improve code performance, readability, and maintainability.
- **Educational Feedback:** Explains complex code segments, making it easier for developers of all skill levels to understand and improve their coding practices.

### How It Works
- **Integration:** Seamlessly integrates with GitHub, analyzing code as changes are made.
- **LLM Usage:** Leverages Llama, a state-of-the-art and free LLM, to understand and analyze code contextually.
- **Feedback Generation:** Automatically posts detailed and constructive feedback directly on the GitHub pull request.

## Getting Started

### Prerequisites
- GitHub Account
- Access to GitHub Actions
- Llama API Key
- Personal Access Token with repo access
### 1. workflow permissions
Configure "Workflow permissions" inside your repository settings (Code and automation > Actions > General). 
[https://github.com/{org}/{repo}/settings/actions](https://github.com/username/repo-name/settings/actions)

"Workflow permissions" to Read and write permissions

### 2. configure llama api key
Configure an LLAMA_API_KEY secret inside your repository settings (Security > Secrets and variables > Actions) . https://github.com/{org}/{repo}/settings/secrets/actions

 - Add your llama API key from the API key section (https://docs.llama-api.com/api-token)

# Setup

## 1. Add a workflow like this in your repo.

Example `.github/workflows/code-review.yml`

```
name: AI Code Review
on: pull_request

jobs:
  code_review:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write    
    steps:
      - uses: actions/checkout@v3
      - name: AI Code Review
        uses: Mamo-00/Code-Patrol@master
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          LLAMA_API_KEY: ${{ secrets.LLAMA_API_KEY }}
```

# Creating Your Own AI-Powered Code Review GitHub Action
## Introduction
This is a step-by-step guide on how to create a GitHub Action similar to the "Code-Patrol," which uses LLMs such as llama or paid versions such as OpenAI for automated code reviews. By following the following steps, you can create a GitHub Action that integrates seamlessly into your development workflow, providing valuable insights and feedback on code commits.

## Design Considerations
Before you start coding, consider the following:

- Purpose: Define what your GitHub Action will achieve. In this case, the action performs automated code reviews using AI.
- Trigger Events: Decide on which GitHub events will trigger the action. Common triggers include push, pull_request, and issue_comment.
- Permissions: Determine the necessary permissions your action needs to function effectively without compromising security.
- External Services: Identify any external APIs or services your action will interact with, such as LLM APIs for code analysis. It is also important to check if the llm you are using is free, because if you use one that is not free and you try to use it in your code without paying, you might get unexplainable issues that is not always easy to figure out, if you are not aware the reason you get these issues are because you didn't pay.

## Step-by-Step Guide
### 1. Set Up Your Action Repository
```
mkdir my-github-action
cd my-github-action
git init
```

### 2. setup your imports 
create a requirements.txt file in your project root with the imports you will be using for your code.

### 3. create your action.yml
Create a action.yml file in the root of your repository. This file contains metadata about your action and defines inputs, outputs, and the main entry point.
```
name: 'AI Code Review'
description: 'Automate code reviews using AI.'
inputs:
  GITHUB_TOKEN:
    description: 'GitHub token for authentication.'
    required: true
  LLAMA_API_KEY:
    description: 'Llama API key for AI responses.'
    required: true

runs:
  using: 'composite'
  steps:
    - name: Checkout
      uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.12'
    - name: Install Dependencies
      run: |
        pip install --upgrade pip
        pip install -r ${{ github.action_path }}/requirements.txt
      shell: bash
    - name: Generate Review
      run: python ${{ github.action_path }}/path/to/code
      shell: bash
      env:
        GITHUB_TOKEN: ${{ inputs.GITHUB_TOKEN }}
        LLAMA_API_KEY: ${{ inputs.LLAMA_API_KEY }}
    - name: Upload Review Results as Artifact
      uses: actions/upload-artifact@v4
      with:
        name: review-results
        path: review_results.txt

```

## 4. implement the Logic
This will be the main logic for your Github Action. You can make other helper functions, I'm just showing you the bare minimum required to make this work. Below is a skeleton for the code. You can also reference my code for inspiration and to help you get started
```
import requests
import os
from llamaapi import LlamaAPI

def fetch_diff_and_analyze():
    # Your code here to interact with GitHub and LLM APIs
    pass

if __name__ == "__main__":
    fetch_diff_and_analyze()
```
## 5. Test your Github action
There are several ways for you to test your github action:
- You can test your code by running your code file in the terminal with `python code.py`.
- Creating a test repository that contains basic boilerplate code such as when running create-react-app, is one way of seeing how it works in action
- You can import the pytest library and run tests on your code
- You can simulate GitHub events using tools like act to run GitHub Actions locally.

## 6. That's It!
Once you are happy with your code, you can push it to your main branch, and people should be able to use your Github Action by adding a workflow similar to the one shown in this readme.
