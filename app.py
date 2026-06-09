"""
app.py — ReflxAI-Advanced
Advanced Streamlit Application: 6-agent engineering platform with professional UI.
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# ── Environment Bootstrap ─────────────────────────────────────────────────────
load_dotenv()

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReflxAI-Advanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Custom CSS ─────────────────────────────────────────────────────────
def _load_css(path: str) -> None:
    """Read and inject a CSS file into the Streamlit app."""
    css_file = Path(path)
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


_load_css("style.css")

# ── Session State Initialisation ──────────────────────────────────────────────
_DEFAULTS: dict = {
    "final_code": "",
    "pr_url": "",
    "selected_template": None,
    "run_triggered": False,
    "auto_run": False,
    "agent_outputs": {},
    "quality_metrics": {},
    "generations_history": [],
    "processing_complete": False,
    "prompt_input": "",
}

for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Template Options ───────────────────────────────────────────────────────────
TEMPLATES: dict[str, str] = {
    "Bubble Sort": (
        "Write a Python function `bubble_sort(arr: list) -> list` that implements "
        "the Bubble Sort algorithm. Include type hints, docstring, and an optimised "
        "early-exit flag to stop if the list becomes sorted before all passes complete."
    ),
    "Inefficient Fibonacci": (
        "Write a deliberately inefficient recursive Fibonacci function "
        "`fib_naive(n: int) -> int` that exhibits exponential time complexity, "
        "then write a second optimised version `fib_memo(n: int) -> int` using "
        "memoization. Include benchmarking code that compares both."
    ),
    "Binary Search": (
        "Write a Python function `binary_search(arr: list, target: int) -> int` "
        "that performs iterative binary search on a sorted list. Return the index "
        "of the target or -1 if not found. Include edge-case handling and a "
        "comprehensive suite of unit tests using the `unittest` module."
    ),
    "Quick Sort": (
        "Write a Python function `quick_sort(arr: list) -> list` implementing "
        "the QuickSort algorithm using a random pivot selection strategy to avoid "
        "worst-case O(n²) behaviour. Include type hints, docstring, and "
        "in-place partitioning logic."
    ),
    "LRU Cache": (
        "Implement an LRU (Least Recently Used) cache class `LRUCache` in Python "
        "with `get(key)` and `put(key, value)` methods, both running in O(1) time. "
        "Use an OrderedDict internally. Include full type hints and a usage example."
    ),
    "REST API Client": (
        "Write a Python class `APIClient` that wraps the `requests` library to "
        "make authenticated REST API calls. Include GET, POST, PUT, DELETE methods, "
        "configurable base URL and API key header, automatic retry logic with "
        "exponential backoff, and timeout handling."
    ),
}

# ── Professional Header ────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="brand-header">
        <div class="brand-logo">🤖</div>
        <div>
            <div class="brand-title">ReflxAI-Advanced</div>
            <div class="brand-subtitle">6-Agent Autonomous Software Engineering Platform</div>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div>
            All Agents Online
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar Settings ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Agent Configuration")
    
    max_iterations = st.slider(
        "Max Generator Iterations",
        min_value=1,
        max_value=5,
        value=2,
        help="How many times should Generator refactor based on feedback?"
    )
    
    st.markdown("**Skip Agents:**")
    skip_test = st.checkbox("Skip Test Generation", value=False)
    skip_perf = st.checkbox("Skip Performance Analysis", value=False)
    skip_security = st.checkbox("Skip Security Audit", value=False)
    skip_docs = st.checkbox("Skip Documentation", value=False)
    
    skip_agents = []
    if skip_test:
        skip_agents.append("test")
    if skip_perf:
        skip_agents.append("performance")
    if skip_security:
        skip_agents.append("security")
    if skip_docs:
        skip_agents.append("docs")

# ── Prompt Form (Always Visible) ──────────────────────────────────────────────
st.markdown('<div class="section-label">⚡ Quick Start Templates</div>', unsafe_allow_html=True)

# Template buttons in columns for better visibility
cols = st.columns(len(TEMPLATES))
for idx, (template_name, template_text) in enumerate(TEMPLATES.items()):
    with cols[idx]:
        if st.button(template_name, use_container_width=True, key=f"template_{template_name}"):
            st.session_state.prompt_input = template_text
            st.session_state.selected_template = template_name
            st.rerun()

st.markdown('<div class="section-label">✍️ Engineering Instructions</div>', unsafe_allow_html=True)

with st.form("engineering_form", clear_on_submit=False):
    prompt_value = st.text_area(
        label="",
        height=180,
        placeholder=(
            "Describe the Python code you want engineered…\n\n"
            "Example: Write a Python function that implements merge sort with O(n log n) "
            "complexity, full type hints, and a comprehensive docstring."
        ),
        help="The Generator Agent will write code to satisfy this specification.",
        value=st.session_state.get("prompt_input", ""),
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.form_submit_button(
            "⚡ Engineer It",
            type="primary",
            use_container_width=True,
        )
    with col2:
        if st.session_state.get("processing_complete"):
            st.markdown(
                "<div style='padding-top: 10px; font-size: 0.75rem; color: #10b981;'>"
                "✅ Auto-generating · Just keep typing…</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='padding-top: 10px; font-size: 0.75rem; color: #64748b;'>"
                "Processing with all agents · Real-time status updates</div>",
                unsafe_allow_html=True,
            )

# Detect if user submitted the form or typed new text
if run_clicked and prompt_value:
    st.session_state.prompt_input = prompt_value
    st.session_state.selected_template = None
    if st.session_state.final_code:
        st.session_state.final_code = ""
        st.session_state.pr_url = ""
        st.session_state.agent_outputs = {}
        st.session_state.quality_metrics = {}
        st.session_state.generations_history = []
        st.session_state.processing_complete = False
    st.session_state.auto_run = True
    st.rerun()
elif prompt_value and prompt_value != st.session_state.get("prompt_input"):
    # User typed new text (not from form submission)
    st.session_state.prompt_input = prompt_value
    st.session_state.selected_template = None
    if st.session_state.final_code:
        st.session_state.final_code = ""
        st.session_state.pr_url = ""
        st.session_state.agent_outputs = {}
        st.session_state.quality_metrics = {}
        st.session_state.generations_history = []
        st.session_state.processing_complete = False
    st.session_state.auto_run = True
    st.rerun()

# ── GitHub Integration ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">🔗 GitHub Integration (Optional)</div>', unsafe_allow_html=True)
github_url = st.text_input(
    label="",
    value="",
    placeholder="https://github.com/your-username/your-repo",
    help=(
        "If provided, the approved code will be committed to a new branch "
        "'ai/engineered-solution' and a Pull Request will be opened automatically."
    ),
)

# ── Agent Execution ───────────────────────────────────────────────────────────
auto_run = st.session_state.get("auto_run", False)
if not st.session_state.get("processing_complete") and (run_clicked or auto_run) and prompt_value.strip():
    # Reset auto_run flag after use
    st.session_state.auto_run = False
    
    st.session_state.final_code = ""
    st.session_state.pr_url = ""
    st.session_state.agent_outputs = {}
    st.session_state.generations_history = []

    from agent_loop import run_developer_agents

    final_code = ""
    generation_count = 0

    with st.status("🚀 Initialising agent pipeline…", expanded=True) as status_box:
        try:
            for status_msg, current_code, agent_outputs in run_developer_agents(
                prompt=prompt_value,
                max_iterations=max_iterations,
                skip_agents=skip_agents,
            ):
                status_box.update(label=status_msg)
                final_code = current_code
                st.session_state.agent_outputs = agent_outputs

                # Track generations
                if "Iteration" in status_msg or "Generator" in status_msg:
                    if current_code and current_code not in [g.get("code") for g in st.session_state.generations_history]:
                        generation_count += 1
                        st.session_state.generations_history.append({
                            "iteration": generation_count,
                            "status": status_msg,
                            "code": current_code,
                            "timestamp": datetime.now().isoformat()
                        })

                time.sleep(0.1)

            status_box.update(label="✅ Engineering complete!", state="complete")
            st.session_state.processing_complete = True
            st.session_state.prompt_input = ""  # Clear the prompt after processing

        except EnvironmentError as env_err:
            status_box.update(label="❌ Configuration error", state="error")
            st.error(f"**Environment Error:** {env_err}")
            st.info(
                "Make sure `GROQ_API_KEY` is set in your `.env` file or "
                "Streamlit secrets (`st.secrets`)."
            )
            st.stop()

        except RuntimeError as rt_err:
            status_box.update(label="❌ Agent error", state="error")
            st.error(f"**Agent Error:** {rt_err}")
            st.stop()

    st.session_state.final_code = final_code
    st.session_state.processing_complete = True
    st.rerun()

# ── Results Dashboard ─────────────────────────────────────────────────────────
if st.session_state.final_code:
    st.markdown("---")
    
    st.markdown("")
    
    # ── Generations Timeline ──────────────────────────────────────────────────
    if st.session_state.generations_history:
        with st.expander("📜 All Generations Timeline", expanded=False):
            st.markdown("### Generation History")
            
            for gen in st.session_state.generations_history:
                with st.container():
                    col1, col2 = st.columns([1, 8])
                    with col1:
                        st.markdown(f"**Iteration {gen['iteration']}**")
                    with col2:
                        st.markdown(f"_{gen['status']}_")
                    
                    with st.expander("View Code", expanded=False):
                        st.code(gen['code'], language="python")
                    st.divider()
    
    # ── Tabs for different outputs ────────────────────────────────────────────
    tab_code, tab_tests, tab_metrics, tab_perf, tab_security, tab_docs = st.tabs([
        "✅ Final Code",
        "🧪 Tests",
        "📊 Metrics",
        "⚡ Performance",
        "🔒 Security",
        "📚 Documentation"
    ])

    # Code Tab
    with tab_code:
        st.markdown("### ✨ Final Implementation")
        st.code(st.session_state.final_code, language="python")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download solution_output.py",
                data=st.session_state.final_code,
                file_name="solution_output.py",
                mime="text/plain",
                use_container_width=True,
            )
        with col2:
            if github_url.strip():
                deploy_clicked = st.button(
                    "🚀 Create Pull Request",
                    type="secondary",
                    use_container_width=True,
                )

                if deploy_clicked:
                    from github_agent import process_github_repo

                    with st.spinner("Committing code and opening Pull Request…"):
                        try:
                            pr_url = process_github_repo(
                                repo_url=github_url.strip(),
                                task_description="Generated code solution",
                                file_contents=st.session_state.final_code,
                            )
                            st.session_state.pr_url = pr_url
                            st.success("Pull Request created!")
                            st.markdown(f"[Open PR ↗]({pr_url})")

                        except EnvironmentError as env_err:
                            st.error(f"**GitHub Token Error:** {env_err}")
                        except ValueError as val_err:
                            st.error(f"**Invalid Repository URL:** {val_err}")
                        except RuntimeError as rt_err:
                            st.error(f"**GitHub Error:** {rt_err}")

    # Tests Tab
    with tab_tests:
        if "tests" in st.session_state.agent_outputs:
            st.markdown("### 🧪 Generated Unit Tests")
            st.code(st.session_state.agent_outputs["tests"], language="python")
            st.download_button(
                label="⬇️ Download test_solution.py",
                data=st.session_state.agent_outputs["tests"],
                file_name="test_solution.py",
                mime="text/plain",
            )
        else:
            st.info("Test generation was skipped or failed.")

    # Metrics Tab
    with tab_metrics:
        if "quality_metrics" in st.session_state.agent_outputs:
            metrics = st.session_state.agent_outputs["quality_metrics"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Overall Score",
                    f"{metrics.get('overall_score', 0)}/100",
                )
            with col2:
                st.metric(
                    "Test Coverage",
                    f"{metrics.get('test_coverage', 0)}%"
                )
            with col3:
                st.metric(
                    "Security Score",
                    f"{metrics.get('security_score', 0)}/100"
                )
            with col4:
                st.metric(
                    "Performance Score",
                    f"{metrics.get('performance_score', 0)}/100"
                )
            
            st.markdown("#### Complexity Analysis")
            complexity = metrics.get("complexity", {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Cyclomatic", complexity.get("cyclomatic_complexity", 0))
            with col2:
                st.metric("Cognitive", complexity.get("cognitive_complexity", 0))
            with col3:
                st.metric("LOC", complexity.get("lines_of_code", 0))
            
            st.markdown(f"**Status:** {metrics.get('approval_status', 'Unknown')}")

    # Performance Tab
    with tab_perf:
        if "performance" in st.session_state.agent_outputs:
            st.markdown("### ⚡ Performance Analysis")
            st.markdown(st.session_state.agent_outputs["performance"])
        else:
            st.info("Performance analysis was skipped or failed.")

    # Security Tab
    with tab_security:
        if "security" in st.session_state.agent_outputs:
            st.markdown("### 🔒 Security Audit")
            audit = st.session_state.agent_outputs["security"]
            if audit.strip().upper() == "SECURE":
                st.success("✅ No vulnerabilities found!")
            else:
                st.warning("⚠️ Security issues detected:")
                st.markdown(audit)
        else:
            st.info("Security audit was skipped or failed.")

    # Documentation Tab
    with tab_docs:
        if "documented_code" in st.session_state.agent_outputs:
            st.markdown("### 📚 Documented Code")
            st.code(st.session_state.agent_outputs["documented_code"], language="python")
            st.download_button(
                label="⬇️ Download documented_solution.py",
                data=st.session_state.agent_outputs["documented_code"],
                file_name="documented_solution.py",
                mime="text/plain",
            )
        else:
            st.info("Documentation generation was skipped or failed.")

    # Export Full Report
    st.markdown("---")
    st.markdown("### 📋 Export Full Report")
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "code": st.session_state.final_code,
        "generations": st.session_state.generations_history,
        "agent_outputs": st.session_state.agent_outputs,
    }
    
    report_json = json.dumps(report_data, indent=2)
    st.download_button(
        label="⬇️ Download Full Report (JSON)",
        data=report_json,
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
    )
    
    # Reset Button
    if st.button("🔄 Start New Generation", type="secondary", use_container_width=False):
        st.session_state.final_code = ""
        st.session_state.pr_url = ""
        st.session_state.agent_outputs = {}
        st.session_state.generations_history = []
        st.session_state.processing_complete = False
        st.rerun()

# ── Professional Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.75rem;color:#94a3b8;padding-bottom:1rem;'>"
    "🤖 ReflxAI-Advanced · 6 Autonomous Agents · Powered by Groq llama3-70b · Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
