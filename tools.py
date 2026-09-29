import json
import subprocess
from pathlib import Path

def list_files(path="."):
    entries = [
        entry.name + ("/" if entry.is_dir() else "")
        for entry in Path(path).iterdir()
    ]
    return "\n".join(sorted(entries)) or "(empty directory)"

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"File {path} not found."

def run_command(command):
    answer = input(f"Run '{command}'? [y/N] ")
    if answer.strip().lower() != "y":
        return "User declined to run this command."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return "Command timed out after 120 seconds."

    output = (result.stdout + result.stderr).strip()
    return f"Exit code: {result.returncode}\n{output or '(no output)'}"


def write_file(path, content):
    file_path = Path(path)

    if file_path.exists():
        answer = input(f"Overwrite '{path}'? [y/N] ")
        if answer.strip().lower() != "y":
            return "User declined to overwrite this file."

    file_path.write_text(content, encoding="utf-8")
    return f"File {path} saved."

AVAILABLE_TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f" tool: {name}({args})")
    try:
        return str(AVAILABLE_TOOLS[name](**args))
    except Exception as e:
        return f"Error running tool {name}: {e}"
