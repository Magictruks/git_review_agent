import os
import sys
from github import Github
from google import genai

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

client = genai.Client(api_key=GEMINI_API_KEY)
gh = Github(GITHUB_TOKEN)

def get_review_from_gemini(diff_content):
    # Prompt en Anglais avec critères spécifiques et notation
    prompt = f"""
    Act as a Senior Fullstack Developer and Security Expert. Analyze the following code diff.
    
    Provide a review based on these 3 criteria:
    1. **Best Practices**: Code quality, readability, naming conventions, and architectural patterns.
    2. **Security**: Potential vulnerabilities, sensitive data exposure, or unsafe logic.
    3. **Performance**: Efficiency, potential memory leaks, or unnecessary computations.

    For each criterion, provide:
    - A score out of 5 (e.g., [Score: 4/5]).
    - A brief justification or specific suggestions for improvement.

    If the diff contains only minor or irrelevant changes, be very concise.
    If a criterion is perfectly met, give 5/5 and a short compliment.

    Format your response clearly using Markdown.

    GIT DIFF:
    {diff_content}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def post_comment(comment):
    if not comment:
        return

    repo = gh.get_repo(REPO_NAME)
    pr = repo.get_pull(int(PR_NUMBER))

    # On ajoute un titre sympa au commentaire
    formatted_comment = f"## 🤖 Gemini Code Review Report\n\n{comment}"
    pr.create_issue_comment(formatted_comment)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        diff_text = f.read()

    # On ignore le review si le diff est vide
    if not diff_text.strip():
        print("Diff is empty, skipping review.")
        sys.exit(0)

    review = get_review_from_gemini(diff_text)
    post_comment(review)