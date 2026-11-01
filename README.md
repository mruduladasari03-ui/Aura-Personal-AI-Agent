# ✨ Aura — Personal AI Agent

Aura is a personal AI workspace built with **Python, Streamlit, OpenAI and SQLite**. It combines an AI chat assistant with practical tools for tasks, goals, memory, daily planning and text summarization.

## Features

- **AI Chat:** natural-language conversations with tool calling.
- **Task Manager:** create, prioritize, complete, reopen and delete tasks.
- **Daily Planner:** generate a suggested schedule from pending tasks and saved goals.
- **Goal Tracker:** save goals and descriptions.
- **Smart Memory:** save and retrieve facts or preferences when explicitly requested.
- **Notes:** store notes locally.
- **AI Summarizer:** summarize pasted text into bullets, study notes, paragraphs or action items.
- **Local database:** tasks, goals, memories and notes are stored in SQLite on your machine.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python |
| User interface | Streamlit |
| AI model | OpenAI API (configurable) |
| Agent tools | OpenAI function/tool calling |
| Database | SQLite |
| Configuration | python-dotenv |

## Project structure

```text
Aura-Personal-AI-Agent/
├── app.py              # Streamlit user interface
├── agent.py            # AI agent, prompts and tool calling
├── database.py         # SQLite database and CRUD operations
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore
├── .streamlit/
│   └── config.toml    # Lavender light theme
├── README.md
└── data/
    └── .gitkeep        # Database is created automatically
```

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- Internet connection for AI requests

## Setup in VS Code

### 1. Download or clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Aura-Personal-AI-Agent.git
cd Aura-Personal-AI-Agent
```

Or download the ZIP, extract it, and open the folder in VS Code.

### 2. Create a virtual environment

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Make a copy of `.env.example` and name it `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder:

```env
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4o-mini
```

Keep `.env` private. **Never upload your API key to GitHub.** The `.gitignore` file excludes it.

### 5. Run Aura

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## Try these prompts

- "Add a task called finish my Python assignment with high priority."
- "Show me my pending tasks."
- "Remember that I prefer concise explanations."
- "Save a goal to build two portfolio projects this semester."
- "Help me plan my day around my pending tasks."
- "Summarize these notes into study points."

## How the AI agent works

1. The user sends a message in the Streamlit chat.
2. `agent.py` sends the conversation and available tool definitions to the OpenAI model.
3. The model decides whether a tool is needed.
4. Aura executes the selected local Python function.
5. The tool result is returned to the model.
6. The model writes a final response for the user.

Available tools:

- `add_task`
- `list_tasks`
- `add_goal`
- `save_memory`
- `get_memory`

## Data and privacy

- SQLite data is stored in `data/aura.db` on your computer.
- The database is created automatically on first launch.
- Chat messages are kept in the current Streamlit session; this starter version does not persist chat history.
- Prompts sent to the AI features are processed by the configured OpenAI API.
- Do not enter passwords, financial credentials, or other highly sensitive information.
- Delete `data/aura.db` if you want to remove all locally stored Aura tasks, goals, memories and notes.

## Current limitations

- This is a local single-user starter application, not a hosted multi-user service.
- The daily planner creates suggestions; it does not access your calendar.
- The agent does not send emails, make purchases, or perform external actions.
- Memory is explicitly saved by the user through the agent or Memory page; it is not automatic.

## Troubleshooting

**`OPENAI_API_KEY is missing`**
- Confirm `.env` exists in the project root.
- Check that the key is assigned to `OPENAI_API_KEY`.
- Restart Streamlit after editing `.env`.

**`ModuleNotFoundError`**
- Activate your virtual environment.
- Run `python -m pip install -r requirements.txt`.

**Streamlit command not found**
- Run `python -m streamlit run app.py`.

**API errors**
- Check your internet connection and API key.
- Confirm your API account has access and available billing/credits for the selected model.

## Roadmap ideas

- Add calendar integration and reminders.
- Add document/PDF question answering with retrieval-augmented generation (RAG).
- Add voice input and text-to-speech.
- Add user authentication before deploying for multiple users.
- Add automated tests and deployment.

## License

This project is provided for learning and portfolio use. Add a license file if you choose to distribute it publicly.
