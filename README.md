# Agentickh

A minimal coding agent powered by Google Gemini 2.0 Flash.

The agent can autonomously read, write, and execute Python code inside a 
sandboxed `calculator/` directory — no manual intervention required. It 
runs an agentic loop where the model decides which tools to call, acts on 
the results, and repeats until it has enough information to respond.

## How it works

1. You send a prompt
2. Gemini picks a tool → the agent runs it → the result is fed back to Gemini
3. Repeat (up to 20 steps) until Gemini returns a plain text answer

## Available tools

| Tool | What it does |
|---|---|
| `get_files_info` | List directory contents |
| `get_file_content` | Read a file |
| `run_python_file` | Execute a `.py` file |
| `write_file` | Write or overwrite a file |

## Stack

- `google-genai` — Gemini 2.0 Flash API
- `python-dotenv` — API key management
- `uv` — dependency and environment management

## Getting started

```bash
# Install dependencies
uv sync

# Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the agent
uv run main.py
```

## Example prompt

```
"Check what's in the calculator directory, 
read the main file, and add a multiply function"
```