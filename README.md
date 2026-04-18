# agentickh

A coding agent built on Google Gemini that can read, write, and execute files within a scoped directory.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file:
   ```
   GEMINI_API_KEY=<your key>
   ```

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py --verbose "your prompt here"
```

The `--verbose` flag prints each tool call with its arguments and response.

## How it works

The agent uses `gemini-2.0-flash-001` in a tool-use feedback loop (up to 20 steps). On each step it can call any of four tools — list files, read a file, write a file, or run a Python file — all scoped to the `./calculator/` directory. It keeps calling tools until it produces a final text response.
