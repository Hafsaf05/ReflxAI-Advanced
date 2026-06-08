"""
agent_loop.py — ReflxAI-Advanced
Multi-Agent Orchestration Engine: coordinates the Generator and Critic agents
in an iterative refinement loop, yielding live status updates to the frontend.
"""

from typing import Generator, Tuple

from generator import generate_code
from critique import evaluate_code, is_approved

# Type alias for the yielded tuple: (status_message, current_code)
AgentUpdate = Tuple[str, str]


def run_developer_agents(
    prompt: str,
    max_iterations: int = 3,
) -> Generator[AgentUpdate, None, None]:
    """
    Orchestrate an iterative debate between the Generator and Critic agents.

    Each iteration:
      1. Generator writes (or rewrites) the code.
      2. Critic evaluates the code.
      3. If APPROVED → loop exits and final code is surfaced.
         If not      → the critique is fed back to the Generator as context.

    This is a generator function that yields (status_message, code) tuples at
    each significant step so the Streamlit frontend can update live.

    Args:
        prompt:         Natural-language description of the code to build.
        max_iterations: Maximum number of generate→review cycles (default: 3).

    Yields:
        Tuples of (str, str) where the first element is a human-readable
        status message and the second is the current code snapshot.

    Raises:
        ValueError: If prompt is empty or max_iterations < 1.
        RuntimeError: Propagated from generator or critique modules on API failure.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")
    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1.")

    current_code: str = ""
    previous_critique: str = ""

    for iteration in range(1, max_iterations + 1):

        # ── Step 1: Generate / Refactor ──────────────────────────────────────
        if iteration == 1:
            generation_prompt = prompt.strip()
            status_gen = "🤖 Generator Agent — Writing baseline implementation…"
        else:
            # Enrich prompt with the previous critique to guide refactoring
            generation_prompt = (
                f"{prompt.strip()}\n\n"
                f"--- PREVIOUS IMPLEMENTATION ---\n{current_code}\n\n"
                f"--- REVIEWER FEEDBACK (fix ALL of these) ---\n{previous_critique}\n\n"
                "Rewrite the code completely to address every point of feedback above."
            )
            status_gen = (
                f"🔧 Generator Agent — Iteration {iteration}: "
                "Refactoring based on reviewer feedback…"
            )

        yield (status_gen, current_code)

        current_code = generate_code(generation_prompt)
        yield (
            f"✅ Generator Agent — Iteration {iteration} complete. Code produced.",
            current_code,
        )

        # ── Step 2: Critique ─────────────────────────────────────────────────
        yield (
            f"🔍 Critic Agent — Iteration {iteration}: Reviewing the implementation…",
            current_code,
        )

        verdict = evaluate_code(current_code)

        if is_approved(verdict):
            yield (
                f"🏆 Critic Agent — APPROVED on iteration {iteration}! "
                "Code passes all quality checks.",
                current_code,
            )
            return  # Exit generator — final code is the last yielded code

        # Not approved — surface the critique and loop
        previous_critique = verdict
        yield (
            f"📋 Critic Agent — Iteration {iteration}: Issues found. "
            f"Sending feedback to Generator for revision…\n\n**Critique:**\n{verdict}",
            current_code,
        )

    # ── Max iterations reached without approval ───────────────────────────────
    yield (
        f"⚠️ Orchestrator — Max iterations ({max_iterations}) reached. "
        "Returning best available implementation.",
        current_code,
    )