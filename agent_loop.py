"""
agent_loop.py — ReflxAI-Advanced
Multi-Agent Orchestration Engine: coordinates all 6 agents in an intelligent
sequence with live status updates to the frontend.
"""

from typing import Generator, Tuple, Dict, Any

from generator import generate_code
from critique import evaluate_code, is_approved
from test_agent import generate_tests
from performance_agent import analyze_performance, is_optimized
from security_agent import audit_security, is_secure
from documentation_agent import generate_documentation
from metrics import generate_quality_report

# Type alias for the yielded tuple: (status_message, current_code, agent_outputs)
AgentUpdate = Tuple[str, str, Dict[str, Any]]


def run_developer_agents(
    prompt: str,
    language: str = "Python",
    max_iterations: int = 3,
    skip_agents: list = None,
) -> Generator[AgentUpdate, None, None]:
    """
    Orchestrate a multi-agent pipeline with intelligent sequencing.

    Pipeline stages:
      1. Generator writes code
      2. Critic reviews for quality
      3. Test Agent generates tests
      4. Performance Agent optimizes
      5. Security Agent audits
      6. Documentation Agent adds docs

    Each stage runs sequentially with live status updates.

    Args:
        prompt:       Natural-language description of the code to build.
        max_iterations: Max generate→critic cycles before proceeding (default: 3).
        skip_agents:  List of agent names to skip ['test', 'performance', 'security', 'docs'].

    Yields:
        Tuples of (status_msg, code, agent_outputs_dict).

    Raises:
        ValueError: If prompt is empty or max_iterations < 1.
        RuntimeError: Propagated from agent modules on API failure.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")
    if max_iterations < 1:
        raise ValueError("max_iterations must be at least 1.")

    skip_agents = skip_agents or []
    agent_outputs: Dict[str, Any] = {}

    current_code: str = ""
    previous_critique: str = ""

    # ── Phase 1: Generate & Review Loop ──────────────────────────────────────
    for iteration in range(1, max_iterations + 1):

        if iteration == 1:
            generation_prompt = prompt.strip()
            status_gen = "🤖 Generator Agent — Writing baseline implementation…"
        else:
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

        yield (status_gen, current_code, agent_outputs)

        current_code = generate_code(generation_prompt, language)
        yield (
            f"✅ Generator Agent — Iteration {iteration} complete.",
            current_code,
            agent_outputs,
        )

        # Review phase
        yield (
            f"🔍 Critic Agent — Iteration {iteration}: Reviewing…",
            current_code,
            agent_outputs,
        )

        verdict = evaluate_code(current_code, language)
        agent_outputs["critic"] = verdict

        if is_approved(verdict):
            yield (
                f"🏆 Critic Agent — APPROVED on iteration {iteration}!",
                current_code,
                agent_outputs,
            )
            break

        previous_critique = verdict
        yield (
            f"📋 Critic Agent — Iteration {iteration}: Issues found.",
            current_code,
            agent_outputs,
        )

    # ── Phase 2: Specialized Agents (Sequential) ────────────────────────────

    # Test Agent
    if "test" not in skip_agents:
        yield ("🧪 Test Agent — Generating comprehensive tests…", current_code, agent_outputs)
        try:
            tests = generate_tests(current_code, language)
            agent_outputs["tests"] = tests
            yield (
                "✅ Test Agent — Tests generated successfully.",
                current_code,
                agent_outputs,
            )
        except Exception as e:
            agent_outputs["tests_error"] = str(e)
            yield (f"⚠️ Test Agent — Error: {str(e)}", current_code, agent_outputs)

    # Performance Agent
    if "performance" not in skip_agents:
        yield (
            "⚡ Performance Agent — Analyzing for optimizations…",
            current_code,
            agent_outputs,
        )
        try:
            perf_analysis = analyze_performance(current_code, language)
            agent_outputs["performance"] = perf_analysis
            yield (
                "✅ Performance Agent — Analysis complete.",
                current_code,
                agent_outputs,
            )
        except Exception as e:
            agent_outputs["performance_error"] = str(e)
            yield (f"⚠️ Performance Agent — Error: {str(e)}", current_code, agent_outputs)

    # Security Agent
    if "security" not in skip_agents:
        yield (
            "🔒 Security Agent — Auditing for vulnerabilities…",
            current_code,
            agent_outputs,
        )
        try:
            security_audit = audit_security(current_code, language)
            agent_outputs["security"] = security_audit
            yield (
                "✅ Security Agent — Audit complete.",
                current_code,
                agent_outputs,
            )
        except Exception as e:
            agent_outputs["security_error"] = str(e)
            yield (f"⚠️ Security Agent — Error: {str(e)}", current_code, agent_outputs)

    # Documentation Agent
    if "docs" not in skip_agents:
        yield (
            "📚 Documentation Agent — Adding comprehensive documentation…",
            current_code,
            agent_outputs,
        )
        try:
            documented_code = generate_documentation(current_code, language)
            agent_outputs["documented_code"] = documented_code
            current_code = documented_code
            yield (
                "✅ Documentation Agent — Documentation added.",
                current_code,
                agent_outputs,
            )
        except Exception as e:
            agent_outputs["docs_error"] = str(e)
            yield (f"⚠️ Documentation Agent — Error: {str(e)}", current_code, agent_outputs)

    # ── Phase 3: Quality Metrics ─────────────────────────────────────────────
    yield ("📊 Calculating quality metrics…", current_code, agent_outputs)

    tests = agent_outputs.get("tests", "")
    security = agent_outputs.get("security", "SECURE")
    perf = agent_outputs.get("performance", "OPTIMIZED")
    approved = is_approved(agent_outputs.get("critic", ""))

    quality_report = generate_quality_report(
        code=current_code,
        tests=tests,
        security_audit=security,
        performance_analysis=perf,
        approval_status=approved,
    )
    agent_outputs["quality_metrics"] = quality_report

    yield (
        "✅ Pipeline complete! All agents have processed the code.",
        current_code,
        agent_outputs,
    )