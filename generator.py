"""
generator.py — ReflxAI-Advanced
Code-Writer Agent: generates production-ready Python code via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_SYSTEM_PROMPT = (
    "You are an elite principal software engineer with 20+ years of experience. "
    "Your sole responsibility is to write clean, production-ready Python code. "
    "Return ONLY the raw Python code — no conversational chatter, no introductory remarks, "
    "no explanatory text, no markdown code fences, and no trailing summaries. "
    "The output must be valid Python that can be saved directly to a .py file and executed. "
    "Follow PEP 8 style conventions, include type hints, and add concise inline comments "
    "where they genuinely aid comprehension."
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


def generate_code(prompt: str) -> str:
    """
    Generate production-ready Python code for the given natural-language prompt.

    Args:
        prompt: A description of the Python code to generate.

    Returns:
        A string containing only valid Python source code.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the API call fails or returns an empty response.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")

    client = _get_client()

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt.strip()},
            ],
            temperature=0.25,   # Low temperature for deterministic, precise code
            max_tokens=4096,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during code generation: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during code generation.")

    raw_output: str = choices[0].message.content.strip()

    # Strip any accidental markdown fences the model might emit despite instructions
    raw_output = _strip_code_fences(raw_output)

    return raw_output


def _strip_code_fences(text: str) -> str:
    """Remove markdown triple-backtick fences if the model accidentally includes them."""
    lines = text.splitlines()

    # Remove leading fence line (e.g. ```python or ```)
    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    # Remove trailing fence line
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()