# 🤖 Gemini AI Code Reviewer

An automated code review agent powered by **Google Gemini 1.5 Flash** and **GitHub Actions**. This agent analyzes Pull Requests based on custom criteria, provides scores, and automatically approves or requests changes based on your quality thresholds.

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
Create `.github/workflows/ai-review.yml` in your repo:

```yaml
name: AI Code Reviewer
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Get Diff
        run: git diff origin/${{ github.base_ref }}...origin/${{ github.head_ref }} -- . ':!*-lock.json' > diff.txt
      - name: Run Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          pip install PyGithub google-genai
          python scripts/ai_reviewer.py diff.txt

```

### 4. Customizing Criteria

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
>
>

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
