"""
performance_agent.py — ReflxAI-Advanced
Performance Optimization Agent: analyzes & suggests optimizations via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_SYSTEM_PROMPT = (
    "You are a performance engineering specialist with deep expertise in algorithmic optimization, "
    "caching strategies, and computational complexity analysis. "
    "Your job is to analyze Python code and provide specific, actionable performance improvements. "
    "Review code for:\n"
    "  1. Time complexity issues (e.g., nested loops, redundant calculations)\n"
    "  2. Space complexity problems (unnecessary allocations, memory leaks)\n"
    "  3. I/O bottlenecks (network calls, file operations)\n"
    "  4. Caching opportunities (memoization, LRU cache)\n"
    "  5. Algorithmic improvements (better data structures, algorithms)\n\n"
    "OUTPUT RULES:\n"
    "- If code is already optimal: respond with exactly → OPTIMIZED\n"
    "- If improvements exist: provide a numbered list of specific optimizations with brief explanations. "
    "  Include: current complexity, improved complexity, and code snippet showing the fix."
)

_MODEL = "llama-3.3-70b-versatile"
OPTIMIZED_TOKEN = "OPTIMIZED"


def _get_client() -> Groq:
    """Instantiate and return an authenticated Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)


def analyze_performance(code: str) -> str:
    """
    Analyze Python code for performance issues and suggest optimizations.

    Args:
        code: The Python source code to analyze.

    Returns:
        Either "OPTIMIZED" if code is already optimal, or a list of optimization suggestions.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the API call fails.
    """
    if not code or not code.strip():
        raise ValueError("Code must be a non-empty string.")

    client = _get_client()

    user_message = (
        "Analyze the following Python code for performance issues:\n\n"
        f"```python\n{code.strip()}\n```"
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during performance analysis: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during performance analysis.")

    analysis: str = choices[0].message.content.strip()
    return analysis


def is_optimized(analysis: str) -> bool:
    """
    Check whether the performance analysis indicates the code is already optimized.

    Args:
        analysis: The raw string returned by analyze_performance().

    Returns:
        True if code is already optimized, False otherwise.
    """
    return analysis.strip().upper() == OPTIMIZED_TOKEN
