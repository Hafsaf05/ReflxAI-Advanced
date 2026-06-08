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
├── app.py              # Streamlit UI entrypoint
├── agent_loop.py       # Multi-agent orchestration engine
├── generator.py        # Code-Writer Agent (Groq)
├── critique.py         # Code-Reviewer Agent (Groq)
├── github_agent.py     # GitHub PR automation (PyGithub)
├── style.css           # Premium light-theme dashboard styles
├── requirements.txt    # Python dependencies
└── .gitignore          # Ignores secrets, venv, cache
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

### Basic — Generate Code

1. Type your engineering instructions in the prompt box  
   *e.g. "Write a Python function for binary search with O(log n) complexity"*
2. Or click a **Quick Start Template** pill to auto-fill a prompt
3. Hit **⚡ Engineer It**
4. Watch the multi-agent pipeline run live in the status panel
5. Download the approved `solution_output.py`

### Advanced — Auto-Deploy to GitHub

1. Generate code as above
2. Paste your GitHub repo URL into the **GitHub Repository URL** field  
   *e.g. `https://github.com/your-username/your-repo`*
3. After code is approved, click **🚀 Create Pull Request**
4. A new branch `ai/engineered-solution` is created with your code committed as `solution_output.py`
5. A Pull Request is automatically opened — click the link to review it

### LeetCode Problems

Paste any LeetCode problem description directly into the prompt:

```
Given an array of integers nums and an integer target, return indices 
of the two numbers such that they add up to target. You may assume 
that each input would have exactly one solution. Solve in O(n) using 
a hash map.
```

The agents will generate an optimised solution, review it for correctness and efficiency, and refine if needed.

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