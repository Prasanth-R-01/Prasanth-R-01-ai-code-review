import textwrap


def shorten_text(s: str, max_chars: int) -> str:
    if len(s) <= max_chars:
        return s
    # keep head and tail to preserve context
    head = s[: max_chars // 2]
    tail = s[-(max_chars // 2) :]
    return head + "\n\n...\n\n" + tail


def build_prompt(snippets):
    header = (
        "You are an experienced Python code reviewer. Provide a concise review with:\n"
        "- A short summary of issues\n"
        "- 3-6 prioritized suggestions (bug risk, readability, style, testing)\n"
        "- Example fixes or short code snippets where helpful\n\n"
        "Review these changed files:\n\n"
    )

    chunks = [header]
    for s in snippets:
        chunks.append(f"File: {s['path']}\n````python\n{s['content'][:2000]}\n```\n")

    chunks.append("\nPlease be concise and use bullet points.\n")
    return "\n".join(chunks)


def call_model(client, prompt: str) -> str:
    # Using the OpenAI-compatible client that talks to Hugging Face router
    resp = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct:novita",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2,
    )
    # The object shape follows the OpenAI-compatible client
    try:
        return resp.choices[0].message.content
    except Exception:
        return str(resp)