"""
generator.py — ReflxAI-Advanced
Code-Writer Agent: generates production-ready Python code via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt(language: str) -> str:
    return (
        f"You are an elite principal software engineer with 20+ years of experience. "
        f"Your sole responsibility is to write clean, production-ready {language} code. "
        f"Return ONLY the raw {language} code — no conversational chatter, no introductory remarks, "
        f"no explanatory text, no markdown code fences, and no trailing summaries. "
        f"The output must be valid {language} that can be saved directly to a file and executed. "
        f"Follow idiomatic style conventions for {language}, include type hints (if applicable), and add concise inline comments "
        f"where they genuinely aid comprehension."
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


def generate_code(prompt: str, language: str = "Python") -> str:
    """
    Generate production-ready code for the given natural-language prompt in the specified language.

    Args:
        prompt: A description of the code to generate.
        language: The programming language to use (default: Python).

    Returns:
        A string containing only valid source code.

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
                {"role": "system", "content": get_system_prompt(language)},
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