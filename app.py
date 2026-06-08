"""
app.py — ReflxAI-Advanced
Streamlit Application Entrypoint: premium multi-agent software engineering UI.
"""

import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ── Environment Bootstrap ─────────────────────────────────────────────────────
load_dotenv()

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReflxAI-Advanced",
    page_icon="R",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject Custom CSS ─────────────────────────────────────────────────────────
def _load_css(path: str) -> None:
    """Read and inject a CSS file into the Streamlit app."""
    css_file = Path(path)
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at: {path}")


_load_css("style.css")

# ── Session State Initialisation ──────────────────────────────────────────────
_DEFAULTS: dict = {
    "final_code": "",
    "pr_url": "",
    "selected_template": None,
    "run_triggered": False,
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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="brand-header">
        <div class="brand-logo">R</div>
        <div>
            <div class="brand-title">ReflxAI-Advanced</div>
            <div class="brand-subtitle">Autonomous Multi-Agent Software Engineering</div>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div>
            Agents Online
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Quick Templates (Pills) ───────────────────────────────────────────────────
st.markdown('<div class="section-label">Quick Start Templates</div>', unsafe_allow_html=True)

selected_pill = st.pills(
    label="templates",
    options=list(TEMPLATES.keys()),
    selection_mode="single",
    label_visibility="collapsed",
    key="pill_selector",
)

# When a template pill is selected, update the prompt and rerun
if selected_pill and selected_pill != st.session_state.get("selected_template"):
    st.session_state.selected_template = selected_pill
    st.session_state.prompt_input = TEMPLATES[selected_pill]
    st.rerun()


# ── Prompt Input ──────────────────────────────────────────────────────────────
# ── Prompt Input + Submit ─────────────────────────────────────────────────────

with st.form("engineering_form", clear_on_submit=True):
    prompt_value = st.text_area(
        label="Engineering Instructions",
        height=180,
        placeholder=(
            "Describe the Python code you want engineered…\n\n"
            "Example: Write a Python function that implements merge sort with O(n log n) "
            "complexity, full type hints, and a comprehensive docstring."
        ),
        help="The Generator Agent will write code to satisfy this specification.",
    )

    run_clicked = st.form_submit_button(
        "⚡ Engineer It",
        type="primary",
        use_container_width=True,
    )

if prompt_value:
    st.session_state.selected_template = None

# ── GitHub Deployment Input ───────────────────────────────────────────────────
st.markdown("")
github_url = st.text_input(
    label="GitHub Repository URL (optional)",
    value="",
    placeholder="https://github.com/your-username/your-repo",
    help=(
        "If provided, the approved code will be committed to a new branch "
        "'ai/engineered-solution' and a Pull Request will be opened automatically."
    ),
)

# # ── Run Controls ──────────────────────────────────────────────────────────────
# col_btn, col_hint = st.columns([1, 3])

# with col_btn:
#     run_clicked = st.button(
#         "⚡ Engineer It",
#         type="primary",
#         use_container_width=True,
#         disabled=not prompt_value.strip(),
#     )

# with col_hint:
#     st.markdown(
#         "<div style='padding-top:10px;font-size:0.78rem;color:#64748b;'>"
#         "Up to 3 agent iterations · Groq llama3-70b-8192</div>",
#         unsafe_allow_html=True,
#     )

# ── Agent Execution ───────────────────────────────────────────────────────────
if run_clicked and prompt_value.strip():
    # Reset previous outputs
    st.session_state.final_code = ""
    st.session_state.pr_url = ""

    from agent_loop import run_developer_agents

    final_code = ""

    with st.status("🚀 Initialising agent pipeline…", expanded=True) as status_box:
        try:
            for status_msg, current_code in run_developer_agents(
                prompt=prompt_value,
                max_iterations=2,  # Set to 1 for faster feedback; increase for more refinement cycles
            ):
                status_box.update(label=status_msg)

                if current_code:
                    final_code = current_code
                    with st.expander("📄 Current Code Snapshot", expanded=False):
                        st.code(current_code, language="python")

                time.sleep(0.1)  # Brief pause for UI responsiveness

            status_box.update(label="✅ Engineering complete!", state="complete")

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

    if "prompt_input" in st.session_state:
        del st.session_state["prompt_input"]

    
    st.session_state.selected_template = None

    st.rerun()

# ── Final Code Output ─────────────────────────────────────────────────────────
if st.session_state.final_code:
    st.markdown("---")
    st.markdown("### ✅ Approved Implementation")

    st.code(st.session_state.final_code, language="python")

    col_copy, col_dl = st.columns(2)
    with col_dl:
        st.download_button(
            label="⬇️ Download solution_output.py",
            data=st.session_state.final_code,
            file_name="solution_output.py",
            mime="text/plain",
            use_container_width=True,
        )

    # ── GitHub PR Deployment ──────────────────────────────────────────────────
    if github_url.strip():
        st.markdown("---")
        st.markdown("### 🐙 GitHub Deployment")

        deploy_clicked = st.button(
            "🚀 Create Pull Request",
            type="secondary",
            use_container_width=False,
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

                except EnvironmentError as env_err:
                    st.error(f"**GitHub Token Error:** {env_err}")
                    st.info("Set `GITHUB_TOKEN` in your `.env` file.")

                except ValueError as val_err:
                    st.error(f"**Invalid Repository URL:** {val_err}")

                except RuntimeError as rt_err:
                    st.error(f"**GitHub Error:** {rt_err}")

    if st.session_state.pr_url:
        st.success("Pull Request created successfully!")
        st.markdown(
            f"""
            <div class="pr-link-container">
                🔗 <a href="{st.session_state.pr_url}" target="_blank">
                {st.session_state.pr_url}
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"[Open Pull Request ↗]({st.session_state.pr_url})",
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.75rem;color:#94a3b8;padding-bottom:1rem;'>"
    "ReflxAI-Advanced · Powered by Groq llama3-70b-8192 · Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)