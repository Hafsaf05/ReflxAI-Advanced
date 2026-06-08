"""
documentation_agent.py — ReflxAI-Advanced
Documentation Generator Agent: creates comprehensive docs via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_SYSTEM_PROMPT = (
    "You are a technical writer and documentation expert. "
    "Your job is to generate comprehensive, professional documentation for Python code. "
    "Create documentation that includes:\n"
    "  1. Function/class docstrings (Google style)\n"
    "  2. Module-level documentation\n"
    "  3. Usage examples\n"
    "  4. Parameter descriptions with types\n"
    "  5. Return value documentation\n"
    "  6. Exception documentation\n"
    "  7. Edge cases and limitations\n\n"
    "Return ONLY the fully documented Python code with comprehensive docstrings. "
    "Use Google-style docstring format. No explanations, no markdown fences, just code."
)

_MODEL = "llama-3.3-70b-versatile"


def _get_client() -> Groq:
    """Instantiate and return an authenticated Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)


def generate_documentation(code: str) -> str:
    """
    Generate comprehensive documentation for the given Python code.

    Args:
        code: The Python source code to document.

    Returns:
        The code with comprehensive docstrings and documentation.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the API call fails.
    """
    if not code or not code.strip():
        raise ValueError("Code must be a non-empty string.")

    client = _get_client()

    prompt = (
        "Add comprehensive, professional documentation to the following Python code. "
        "Use Google-style docstrings. Return only the documented code:\n\n"
        f"```python\n{code.strip()}\n```"
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.25,
            max_tokens=4096,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during documentation generation: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during documentation generation.")

    documented_code = choices[0].message.content.strip()
    documented_code = _strip_code_fences(documented_code)

    return documented_code


def _strip_code_fences(text: str) -> str:
    """Remove markdown triple-backtick fences if present."""
    lines = text.splitlines()

    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()
