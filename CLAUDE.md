# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Requires a `.env` file with:
```
GEMINI_API_KEY=<your key>
```

Dependencies are managed with `uv`. Install with:
```bash
uv sync
```

## Running the Agent

```bash
uv run main.py "your prompt here"
uv run main.py --verbose "your prompt here"
```

`--verbose` prints each function call with its arguments and the full function response.

## Architecture

This is a coding agent built on Google Gemini (`gemini-2.0-flash-001`) with a tool-use feedback loop.

**Entry point:** `main.py` — builds the message history, calls Gemini in a loop (up to `MAX_STEPS=20`), dispatches tool calls, and appends results back as `user` messages until the model produces a final text response.

**Tool layer (`functions/`):**
- Each file exports a `schema_*` (`types.FunctionDeclaration`) and a plain Python function.
- `call_function.py` routes Gemini's `function_call` parts to the right Python function, always injecting `working_directory="./calculator"` so all tool operations are sandboxed to that subdirectory.
- `config.py` holds `MAX_CHARS = 10000`, the read truncation limit used by `get_file_content`.

**Available tools:**
| Tool | Purpose |
|------|---------|
| `get_files_info` | List directory contents with sizes |
| `get_file_content` | Read a file (truncated to MAX_CHARS) |
| `run_python_file` | Execute a `.py` file via subprocess (30s timeout) |
| `write_file` | Write/overwrite a file |

**Target codebase (`calculator/`):** The demo project the agent operates on — a calculator with `main.py`, `pkg/calculator.py`, `pkg/render.py`, and `tests.py`.

## Adding a New Tool

1. Create `functions/my_tool.py` with a `schema_my_tool` (`FunctionDeclaration`) and a `my_tool(working_directory, ...)` function.
2. Import both in `main.py` and add `schema_my_tool` to `available_functions`.
3. Add `"my_tool": my_tool` to the `name_to_func` dict in `functions/call_function.py`.
