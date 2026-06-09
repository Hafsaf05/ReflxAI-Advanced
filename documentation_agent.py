"""
documentation_agent.py — ReflxAI-Advanced
Documentation Generator Agent: creates comprehensive docs via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt(language: str) -> str:
    return (
        "You are a technical writer and documentation expert. "
        f"Your job is to generate comprehensive, professional documentation for {language} code. "
        "Create documentation that includes:\n"
        "  1. Function/class descriptions\n"
        "  2. Module-level documentation\n"
        "  3. Usage examples\n"
        "  4. Parameter descriptions with types\n"
        "  5. Return value documentation\n"
        "  6. Exception documentation\n"
        "  7. Edge cases and limitations\n\n"
        f"Return ONLY the fully documented {language} code with comprehensive docstrings/comments. "
        f"Use standard documentation formats for {language} (e.g., Javadoc for Java, Doxygen for C++, docstrings for Python). No explanations, no markdown fences, just code."
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


def generate_documentation(code: str, language: str = "Python") -> str:
    """
    Generate comprehensive documentation for the given code.

    Args:
        code: The source code to document.
        language: The programming language of the code (default: Python).

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
        f"Add comprehensive, professional documentation to the following {language} code. "
        f"Use standard documentation formats. Return only the documented code:\n\n"
        f"```{language.lower()}\n{code.strip()}\n```"
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": get_system_prompt(language)},
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
