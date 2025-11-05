import os
import subprocess
import json
from openai import OpenAI
from app.utils import build_prompt, call_model, shorten_text




def get_env(name, default=None):
    v = os.environ.get(name, default)
    if v is None:
        raise RuntimeError(f"Required env var {name} not set")
    return v




def git_changed_files(base_sha, head_sha):
    # returns list of changed file paths between base and head
    cmd = ["git", "diff", "--name-only", f"{base_sha}", f"{head_sha}"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("git diff failed:", proc.stderr)
        return []
    files = [f.strip() for f in proc.stdout.splitlines() if f.strip()]
    return files




def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Could not read {path}:", e)
    return None



def main():
    base_sha = os.environ.get("BASE_SHA")
    head_sha = os.environ.get("HEAD_SHA")
    hf_key = os.environ.get("HF_API_KEY")


    if not hf_key:
        print("HF_API_KEY not set. Exiting.")
        return


    if not base_sha or not head_sha:
        print("BASE_SHA or HEAD_SHA not set; attempting to use GITHUB_EVENT_PATH")
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if event_path and os.path.exists(event_path):
            with open(event_path, "r", encoding="utf-8") as f:
                ev = json.load(f)
            base_sha = ev.get("pull_request", {}).get("base", {}).get("sha")
            head_sha = ev.get("pull_request", {}).get("head", {}).get("sha")


    if not base_sha or not head_sha:
        print("Unable to determine base/head SHA. Exiting.")
        return


    print(f"Diffing {base_sha}..{head_sha}")
    changed = git_changed_files(base_sha, head_sha)
    print("Changed files:", changed)

    # filter for code files (change as needed)
    code_files = [f for f in changed if f.endswith(".py")]
    if not code_files:
        print("No python files changed. Exiting.")
        return

    snippets = []
    for path in code_files:
        content = read_file(path)
        if content:
            # include only up to a limit per file to avoid huge prompts
            snippets.append({"path": path, "content": shorten_text(content, 2500)})

    # build the prompt
    prompt = build_prompt(snippets)

    # call the model
    client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_key)
    print("Sending prompt to model (length:", len(prompt), ")")

    try:
        review = call_model(client, prompt)
    except Exception as e:
        print("Model call failed:", e)
        return

    print("\n=== AI CODE REVIEW ===\n")
    print(review)

    # Optionally: post the review as a PR comment using PyGithub (requires GITHUB_TOKEN)
    # To keep the scope small, we simply print the review to action logs.


if __name__ == "__main__":
    main()
