# AI Agent

At Compassion International, we have the opportunity to spend one sprint every six months exploring something we're interested in and want to learn more about. We call this an "Ignite Sprint."

For this Ignite Sprint, I'm diving deeper into AI agents: how they work, how to build and run them locally, and the design decisions involved in putting them together.

## Overview

This repository is a minimal, educational implementation of a local AI agent that demonstrates core agent patterns:
- **Tool calling**: The agent can be equipped with custom tools (functions) to interact with the local filesystem and execute shell commands.
- **Human-in-the-loop safety**: Sensitive actions (running commands, overwriting files) require explicit user approval before execution.
- **Local-first design**: Runs entirely on your machine by connecting to any OpenAI-compatible local LLM server (e.g., Ollama, LM Studio, vLLM).

## Features

- 🔧 **Function/Tool Calling**: Built-in support for OpenAI-style tool schemas, allowing the LLM to request specific actions.
- 🛡️ **Safety & Approval Workflow**: Interactive prompts ensure you approve potentially destructive operations before they run.
- 📦 **Self-contained**: Uses standard Python libraries plus `openai` (for API compatibility), with no heavy framework dependencies.
- 🧠 **Extensible**: Add new tools by registering them in `tools.py` and updating `tool_schemas.json`.

## How It Works

1. **Schema Definition**: Tool definitions are stored in `tool_schemas.json` following the OpenAI function-calling format.
2. **Agent Loop**: `main.py` sends user input to the local LLM, which returns either a text response or a list of tool calls.
3. **Tool Execution**: `tools.py` maps requested tool names to Python functions, executes them, and feeds results back to the model.
4. **Human Verification**: Before running shell commands or overwriting files, the agent pauses and asks for your explicit approval.

## Running Locally

### Prerequisites
- Python 3.12+
- A local LLM server exposing an OpenAI-compatible API (e.g., Ollama running `qwen:latest` on `localhost:8080`)
- `uv` package manager (recommended)

### Setup & Run
```bash
# Install dependencies
uv sync

# Start the agent
uv run main.py
```

### Configuring the Model
Update the `MODEL` variable and `base_url` in `main.py` to match your local LLM setup:
```python
MODEL = "your-model-name"
# ...
with OpenAI(base_url="http://localhost:8080/v1", api_key="local") as client:
```

## Project Structure

```
.
├── main.py          # Agent loop, message handling, and CLI interface
├── tools.py         # Tool implementations and execution router
├── tool_schemas.json # OpenAI-compatible function schemas for the LLM
├── pyproject.toml   # Project metadata and dependencies
├── snake_game/      # Example/sandbox directory
└── README.md        # This file
```

## Design Decisions & Learnings

This prototype explores several key agent architecture choices:
- **Stateful conversation**: Maintains a message history array to preserve context across turns.
- **Schema-driven tools**: Separates tool definitions from implementation, making it easier to swap tools or generate schemas dynamically.
- **Explicit approval gates**: Prevents accidental file modifications or command execution by requiring user confirmation.
- **Lightweight stack**: Avoids heavy agent frameworks to keep the codebase transparent and easy to study.

## License & Attribution

Internal project developed during a Compassion International Ignite Sprint.
