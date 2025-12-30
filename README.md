# 🤖 Gemini AI Code Reviewer

> **AI-powered GitHub Action for automated code reviews, scoring, and PR management using Gemini 2.5 Flash.**

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Magictruks/git_review_agent/.github%2Fworkflows%2Fai_review.yml?label=AI%20Agent&color=red)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)
![Model](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange?logo=google-gemini&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

An automated code review agent powered by **Google Gemini 2.5 Flash** and **GitHub Actions**. This agent analyzes Pull Requests based on custom criteria, provides scores, and automatically approves or requests changes based on your quality thresholds.

## 🚀 Features

- **Automated Reviews**: Triggered on every Pull Request (opened or updated).
- **Multi-Criteria Scoring**: Evaluates code on Best Practices, Security, Performance, and Maintainability.
- **Smart Actions**: 
    - ✅ **Approve**: If the overall score is ≥ 90%.
    - ❌ **Request Changes**: If the overall score is < 50%.
    - 💬 **Comment**: For everything in between.
- **Context-Aware**: Uses Gemini 2.5 Flash's large context window to handle large diffs efficiently.
- **Cost Effective**: Optimized to only scan relevant code changes and ignore noise (lockfiles, assets).

## 🛠️ Architecture



1. **GitHub Action** triggers on `pull_request`.
2. **Git Diff** is extracted and filtered.
3. **Python Script** sends the diff to Gemini API with a strict system prompt.
4. **Agent** submits a formal Review (Approve/Request Changes) back to the PR.

## 📦 Setup

### 1. Prerequisites
- A Google AI Studio API Key ([Get it here](https://aistudio.google.com/)).
- A GitHub repository.

### 2. Configure Secrets
Add the following secret to your GitHub repository (**Settings > Secrets and variables > Actions**):
- `GEMINI_API_KEY`: Your Google Gemini API key.

### 3. Important: Enable Workflow Permissions
By default, GitHub prevents Actions from approving Pull Requests. You must enable this manually:
1. Go to **Settings > Actions > General**.
2. Scroll down to **Workflow permissions**.
3. Check the box **"Allow GitHub Actions to create and approve pull requests"**.
4. Click **Save**.

Without this step, the script will fail with a `422 Unprocessable Entity` error when trying to approve a PR.
### 4. Add the Workflow
To integrate the AI reviewer into your repository, you need to add the workflow file. You can find the complete configuration and use it as a template here:

👉 **[.github/workflows/ai-review.yml](.github/workflows/ai-review.yml)**

This workflow is pre-configured to:
- Trigger on Pull Request events.
- Extract and filter the code diff.
- Execute the Python analysis script with the necessary permissions.

### 5. Customizing Criteria

You can easily adjust the scoring logic and thresholds in `scripts/ai_reviewer.py`:

```python
CONFIG = {
    "criteria": ["Best Practices", "Security", "Performance", "Maintainability"],
    "approve_threshold": 0.90,
    "request_changes_threshold": 0.50
}

```

## 📊 Example Report

> ### ✅ Gemini AI Review Report
>
>
> **Overall Score: 18/20 (90.0%)**
> *Great job! The code meets our high standards.*
>
> 
>**Best Practices [Score: 5/5]**
> * Excellent modularization of the auth service.
>
>
> **Security [Score: 4/5]**
> * Consider adding rate-limiting to the new login endpoint.

## 🤝 Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests. All PRs will be automatically reviewed by our Gemini AI agent.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
