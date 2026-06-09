"""
test_agent.py — ReflxAI-Advanced
Unit Test Generator Agent: creates comprehensive unit tests via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt(language: str) -> str:
    return (
        "You are an elite software testing engineer with expertise in unit testing and test-driven development. "
        f"Your sole responsibility is to generate comprehensive, production-ready unit tests for {language} code. "
        f"Return ONLY raw {language} code using a standard testing framework (e.g., pytest for Python, JUnit for Java, Google Test for C++) — no explanations, no markdown fences, no preamble. "
        "Generate tests that cover:\n"
        "  1. Happy path (normal inputs)\n"
        "  2. Edge cases (boundary values, empty inputs, large inputs)\n"
        "  3. Error cases (invalid inputs, exceptions)\n"
        "  4. Performance expectations (timeout, resource limits)\n"
        "Include assertions, setup/teardown where needed, and parametrized tests for multiple scenarios. "
        f"Output must be valid {language} that compiles and runs directly with the chosen testing framework."
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


def generate_tests(code: str, language: str = "Python") -> str:
    """
    Generate comprehensive unit tests for the given code.

    Args:
        code: The source code to generate tests for.
        language: The programming language of the code (default: Python).

    Returns:
        A string containing valid pytest test code.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the API call fails.
    """
    if not code or not code.strip():
        raise ValueError("Code must be a non-empty string.")

    client = _get_client()

    prompt = (
        f"Generate comprehensive unit tests for the following {language} code:\n\n"
        f"```{language.lower()}\n{code.strip()}\n```\n\n"
        "Return ONLY the test code, ready to compile and run."
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": get_system_prompt(language)},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=4096,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during test generation: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during test generation.")

    test_code = choices[0].message.content.strip()
    test_code = _strip_code_fences(test_code)

    return test_code


def _strip_code_fences(text: str) -> str:
    """Remove markdown triple-backtick fences if present."""
    lines = text.splitlines()

    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()
