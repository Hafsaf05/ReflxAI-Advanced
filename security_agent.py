"""
security_agent.py — ReflxAI-Advanced
Security Auditor Agent: scans for vulnerabilities and suggests hardening via Groq.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt(language: str) -> str:
    return (
        f"You are a senior security engineer with expertise in {language} security, OWASP, and secure coding practices. "
        f"Your job is to audit {language} code for security vulnerabilities and provide hardening recommendations. "
        "Scan for:\n"
        "  1. Injection attacks (SQL, command, eval, pickle)\n"
        "  2. Cryptographic weaknesses (weak hashing, hardcoded secrets, insecure random)\n"
        "  3. Path traversal and file operation risks\n"
        "  4. Authentication/authorization flaws\n"
        "  5. Dependency vulnerabilities (unsafe imports, outdated libraries)\n"
        "  6. Data exposure (hardcoded credentials, debug info, logging sensitive data)\n"
        "  7. Deserialization risks\n\n"
        "OUTPUT RULES:\n"
        "- If no vulnerabilities found: respond with exactly → SECURE\n"
        "- If vulnerabilities exist: provide a numbered list with:\n"
        "  * Vulnerability type and severity (HIGH/MEDIUM/LOW)\n"
        "  * Specific location and explanation\n"
        "  * Recommended fix with code example"
    )

_MODEL = "llama-3.3-70b-versatile"
SECURE_TOKEN = "SECURE"


def _get_client() -> Groq:
    """Instantiate and return an authenticated Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)


def audit_security(code: str, language: str = "Python") -> str:
    """
    Audit code for security vulnerabilities.

    Args:
        code: The source code to audit.
        language: The programming language of the code (default: Python).

    Returns:
        Either "SECURE" if no vulnerabilities found, or a list of issues with recommendations.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
        RuntimeError: If the API call fails.
    """
    if not code or not code.strip():
        raise ValueError("Code must be a non-empty string.")

    client = _get_client()

    user_message = (
        f"Perform a security audit on the following {language} code:\n\n"
        f"```{language.lower()}\n{code.strip()}\n```"
    )

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": get_system_prompt(language)},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
            max_tokens=2048,
        )
    except Exception as exc:
        raise RuntimeError(f"Groq API call failed during security audit: {exc}") from exc

    choices = response.choices
    if not choices or not choices[0].message.content:
        raise RuntimeError("Groq returned an empty response during security audit.")

    audit_result: str = choices[0].message.content.strip()
    return audit_result


def is_secure(audit_result: str) -> bool:
    """
    Check whether the security audit indicates the code is secure.

    Args:
        audit_result: The raw string returned by audit_security().

    Returns:
        True if no vulnerabilities found, False otherwise.
    """
    return audit_result.strip().upper() == SECURE_TOKEN
