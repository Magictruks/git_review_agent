import os
import sys
import re
from github import Github
from google import genai

# --- CONFIGURATION PARAMÉTRABLE ---
CONFIG = {
    "criteria": ["Best Practices", "Security", "Performance", "Maintainability"],
    "max_score_per_criterion": 5,
    "approve_threshold": 0.90,        # 90% pour approuver
    "request_changes_threshold": 0.50 # Moins de 50% pour bloquer
}

# --- INITIALISATION ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = int(os.getenv("PR_NUMBER"))

client = genai.Client(api_key=GEMINI_API_KEY)
gh = Github(GITHUB_TOKEN)

def get_review_from_gemini(diff_content):
    criteria_text = "\n".join([f"- {c}" for c in CONFIG['criteria']])
    max_score = CONFIG['max_score_per_criterion']

    prompt = f"""
    Act as a Senior Software Engineer. Analyze this git diff and provide a technical review.
    
    For each of the following {len(CONFIG['criteria'])} criteria, provide a score out of {max_score}:
    {criteria_text}

    IMPORTANT: Format each score strictly as: [Score: X/{max_score}]
    Provide your reasoning in English. Be concise but impactful.

    GIT DIFF:
    {diff_content}
    """

    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    return response.text

def calculate_stats(review_text):
    max_val = CONFIG['max_score_per_criterion']
    # Regex flexible pour capturer les notes
    scores = re.findall(rf"\[Score:\s*(\d+)/{max_val}\]", review_text)

    if not scores:
        return 0, 0

    total_score = sum(int(s) for s in scores)
    max_possible = len(CONFIG['criteria']) * max_val
    percentage = total_score / max_possible
    return total_score, percentage

def submit_review(review_text, total_score, percentage):
    repo = gh.get_repo(REPO_NAME)
    pr = repo.get_pull(PR_NUMBER)

    max_possible = len(CONFIG['criteria']) * CONFIG['max_score_per_criterion']

    # Construction du message avec indicateur visuel
    if percentage >= CONFIG['approve_threshold']:
        status_icon, event = "✅", "APPROVE"
        summary = "Great job! The code meets our high standards."
    elif percentage < CONFIG['request_changes_threshold']:
        status_icon, event = "❌", "REQUEST_CHANGES"
        summary = "Significant issues found. Please address the points below."
    else:
        status_icon, event = "💬", "COMMENT"
        summary = "Review completed with some suggestions for improvement."

    header = f"## {status_icon} Gemini AI Review Report\n"
    header += f"**Overall Score: {total_score}/{max_possible} ({percentage:.1%})**\n"
    header += f"_{summary}_\n\n---\n"

    full_body = header + review_text
    pr.create_review(body=full_body, event=event)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        diff_text = f.read()

    if len(diff_text.strip()) < 10:
        print("Diff too small, skipping.")
        sys.exit(0)

    content = get_review_from_gemini(diff_text)
    score, pct = calculate_stats(content)
    submit_review(content, score, pct)
