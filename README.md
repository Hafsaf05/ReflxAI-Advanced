# ⚡ ReflxAI-Advanced

> **Multi-Agent AI Code Generation and Review Platform**  
> Powered by Groq · Built with Streamlit · Deploys via GitHub

---

## 🧠 What Is This?

ReflxAI-Advanced is a fully autonomous, self-refining code engineering system. You describe what you want in plain English — a sorting algorithm, a REST client, a LeetCode solution — and a pipeline of AI agents debates, critiques, and refines the code until it's approved. The final output can be automatically committed to your GitHub repo as a Pull Request.

No copy-pasting. No back-and-forth. Just describe → approve → deploy.

---

## ✨ Features

- Multi-agent code generation and review
- Iterative refinement loop (up to 3 passes)
- Live Streamlit status tracking
- Download generated solutions
- GitHub Pull Request automation
- Prebuilt engineering templates
- Groq-powered inference

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│               Streamlit Frontend             │
│    (app.py · style.css · Live Status UI)    │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │  agent_loop.py    │  ← Orchestrator
         │  (3-iteration max)│
         └──────┬──────┬─────┘
                │      │
    ┌───────────▼─┐  ┌─▼────────────┐
    │ generator.py │  │  critique.py │
    │  Code Writer │  │  QA Reviewer │
    │  (Groq LLM)  │  │  (Groq LLM)  │
    └─────────────┘  └──────────────┘
                   │
         ┌─────────▼─────────┐
         │  github_agent.py  │  ← Optional
         │  PR Automation    │
         └───────────────────┘
```

### How The Agent Loop Works

1. **Generator Agent** writes a baseline implementation from your prompt
2. **Critic Agent** reviews it for bugs, inefficiencies, edge cases, and style violations
3. If the Critic returns `APPROVED` → done. If not → feedback is fed back to the Generator
4. Repeats up to **3 iterations** until the code passes review
5. Final approved code is displayed, downloadable, and optionally pushed to GitHub

---

## 📁 Project Structure

```
ReflxAI-Advanced/
├── app.py                  # Enhanced Streamlit UI with tabs & metrics
├── agent_loop.py           # 6-agent orchestration engine
├── generator.py            # Code-Writer Agent (Groq)
├── critique.py             # Code-Reviewer Agent (Groq)
├── test_agent.py           # Unit Test Generator (Groq) [NEW]
├── performance_agent.py    # Performance Optimizer (Groq) [NEW]
├── security_agent.py       # Security Auditor (Groq) [NEW]
├── documentation_agent.py  # Documentation Generator (Groq) [NEW]
├── metrics.py              # Quality Metrics Calculator [NEW]
├── github_agent.py         # GitHub PR automation (PyGithub)
├── style.css               # Premium dashboard styles
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .gitignore              # Ignores secrets, venv, cache
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq Cloud](https://console.groq.com) API key (free)
- *(Optional)* A GitHub Personal Access Token for PR automation

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/ReflxAI-Advanced.git
cd ReflxAI-Advanced

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here   # Optional
```

### Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🎮 Usage

### Basic Workflow

1. **Enter Requirements** in the prompt box or select a template
2. **Configure Agents** in the sidebar (adjust iteration depth, skip agents if needed)
3. **Click "⚡ Engineer It"** to start the pipeline
4. **Watch Live Updates** as agents execute sequentially
5. **Review Outputs** in the multi-tab interface:
   - **Code Tab** — Final implementation with download
   - **Tests Tab** — pytest-compatible unit tests
   - **Metrics Tab** — Quality scores and complexity analysis
   - **Performance Tab** — Optimization recommendations
   - **Security Tab** — Vulnerability audit results
   - **Docs Tab** — Code with comprehensive docstrings

### Advanced Features

#### Agent Configuration (Sidebar)
- **Max Generator Iterations** (1–5) — How many times should the Generator refactor based on Critic feedback?
- **Skip Agents** — Toggle individual agents (Test, Performance, Security, Docs) to speed up pipeline

#### Export Options
- **Download Code** — `solution_output.py` (final code)
- **Download Tests** — `test_solution.py` (pytest file)
- **Download Documented Code** — `documented_solution.py` (with docstrings)
- **Download Full Report** — JSON report with all agent outputs

#### GitHub Integration
1. Paste your GitHub repo URL (e.g., `https://github.com/user/repo`)
2. Click **"🚀 Create Pull Request"** after code approval
3. A new branch `ai/engineered-solution` is created automatically

---

## 📊 Quality Metrics Explained

| Metric | Meaning | Ideal |
|---|---|---|
| **Overall Score** | Weighted average of all metrics (0–100) | 90+ |
| **Cyclomatic Complexity** | Number of decision paths | 1–10 |
| **Cognitive Complexity** | Mental effort to understand code | 1–15 |
| **Test Coverage** | % of functions tested | 80%+ |
| **Security Score** | Absence of vulnerabilities (0–100) | 100 |
| **Performance Score** | Code optimization rating (0–100) | 85+ |
| **Approval Status** | Critic Agent final verdict | ✅ APPROVED |

---

## 🤖 Agent Roles

### Generator Agent
- **Role** — Writes clean, production-ready Python code
- **Refines Based On** — Critic feedback
- **Output** — Raw Python source code

### Critic Agent
- **Role** — Reviews code for quality, bugs, edge cases
- **Verdict** — `APPROVED` or numbered list of issues

### Test Agent
- **Role** — Generates comprehensive unit tests
- **Format** — pytest-compatible with parametrized tests

### Performance Agent
- **Role** — Analyzes code for bottlenecks and optimization opportunities
- **Verdict** — `OPTIMIZED` or numbered list of improvements

### Security Agent
- **Role** — Audits code for vulnerabilities and hardening
- **Checks** — Injection attacks, cryptography, secret exposure
- **Severity Levels** — HIGH/MEDIUM/LOW

### Documentation Agent
- **Role** — Adds comprehensive docstrings and comments
- **Style** — Google-style docstring format

---

## ⚙️ Configuration

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq Cloud API key |
| `GITHUB_TOKEN` | ⬜ Optional | GitHub PAT with `repo` scope for PR creation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit + Custom CSS |
| LLM Backend | Groq Cloud (`llama-3.3-70b-versatile`) |
| GitHub Automation | PyGithub |
| Environment | python-dotenv |

---

## 📋 Quick Start Templates

The UI ships with 6 built-in templates:

- **Bubble Sort** — Optimised with early-exit flag
- **Inefficient Fibonacci** — Naive vs memoized with benchmarking
- **Binary Search** — Iterative with unit tests
- **Quick Sort** — Random pivot to avoid O(n²) worst case
- **LRU Cache** — O(1) get/put using OrderedDict
- **REST API Client** — Full CRUD with retry and backoff

---

## 🔒 Security

- API keys are loaded from `.env` and never hardcoded
- `.gitignore` excludes `.env` and `secrets.toml`
- GitHub tokens are read from environment variables only
- No credentials are ever logged or displayed in the UI

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">
  <strong>ReflxAI-Advanced</strong> · Powered by Groq · Built with Streamlit
</div>