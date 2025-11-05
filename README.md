# AI Code Reviewer

A minimal example that runs an LLM-powered code review when a Pull Request is opened. Uses the Hugging Face Router (OpenAI-compatible API) to call `meta-llama/Llama-3.2-3B-Instruct:novita`.

## Setup
1. Create a repository and copy the files from this repo.
2. Create a secret in your repository: `HF_API_KEY` with your Hugging Face token.
3. Push a branch with some changes (modify `sample_code/main.py` or add new `.py` files).
4. Open a Pull Request — the Action will run automatically.

## How it works
- Workflow triggers on `pull_request` events.
- It builds the Docker image, mounts the repository, and runs `app/review.py`.
- `review.py` diffs the PR's base and head commits, finds changed `.py` files, and sends them to the LLM to get suggestions.

## Notes
- This demo prints the review to action logs. If you want the review posted as a PR comment, enable the PyGithub section in `review.py` and provide `GITHUB_TOKEN` (already available as a built-in secret).
- Keep prompts short. The script truncates large files to keep prompt length reasonable.