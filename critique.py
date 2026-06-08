"""
critique.py — ReflxAI-Advanced
Code-Reviewer Agent: evaluates Python code for bugs, traps, and inefficiencies via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_SYSTEM_PROMPT = (
    "You are a meticulous automated QA engineer and code auditor. "
    "Your job is to review Python code for the following categories of issues:\n"
    "  1. Logical bugs or incorrect algorithmic behavior\n"
    "  2. Runtime errors, unhandled exceptions, or edge-case traps\n"
    "  3. Performance inefficiencies (e.g., O(n²) where O(n log n) is trivial)\n"
    "  4. Security vulnerabilities or unsafe practices\n"
    "  5. Violations of Pythonic style (PEP 8, type hints, readability)\n\n"
    "STRICT OUTPUT RULES:\n"
    "- If the code is correct, efficient, and optimal: respond with EXACTLY one word → APPROVED\n"
    "- If any issues exist: output a clean, numbered, actionable list of specific modifications needed. "
    "  Do NOT include praise, preamble, or closing remarks. Only the numbered list."
)

_MODEL = "llama-3.3-70b-versatile"
APPROVAL_TOKEN = "APPROVED"


def _get_client() -> Groq:
    """Instantiate and return an authenticated Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)


def evaluate_code(code: str) -> str:
    """
    Evaluate a Python code block for quality issues.

    Args:
        code: The Python source code to review.

    Returns:
        The string "APPROVED" if the code passes all checks, or a numbered
        list of required modifications as a plain string.

    Raises:
        ValueError: If the code argument is empty.
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the Groq API call fails.
    """
    if not code or not code.strip():
        raise ValueError("Code block must be a non-empty string.")

    client = _get_client()

    user_message = (
        "Review the following Python code and respond according to your instructions:\n\n"
        f"```python\n{code.strip()}\n```"
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.1,   # Very low temperature for consistent, objective evaluation
            max_tokens=2048,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during code evaluation: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during code evaluation.")

    verdict: str = choices[0].message.content.strip()
    return verdict


def is_approved(verdict: str) -> bool:
    """
    Check whether the reviewer's verdict is an approval.

    Args:
        verdict: The raw string returned by evaluate_code().

    Returns:
        True if the verdict is exactly APPROVED (case-insensitive), False otherwise.
    """
    return verdict.strip().upper() == APPROVAL_TOKEN