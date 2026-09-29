from openai import OpenAI
from pathlib import Path
import tools
import json

MODEL = "qwen"

SYSTEM_PROMPT = (
    "You are a local assistant. Use the available tools when needed "
    "to fulfill requests. When asked to read, list, create, or edit "
    "files, use the corresponding tools without requiring the user "
    "to explicitly name a tool. Base answers about files on their "
    "actual contents, obtained through tools. "
    "Relative paths are resolved from the working directory. "
    "If a tool fails or the user declines an action, explain that "
    "honestly and do not claim the action succeeded."
)

def run_agent(client, messages, tool_schemas):
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tool_schemas,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            return message.content or ""

        for tool_call in message.tool_calls:
            result = tools.run_tool(tool_call)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

def main():
    schema_path = Path(__file__).with_name("tool_schemas.json")
    tool_schemas = json.loads(schema_path.read_text(encoding="utf-8"))

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    with OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="local",
    ) as client:
        print(f"Mini agent ready. Working directory: {Path.cwd()}")
        print("Type 'exit' to quit.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue

            messages.append({
                "role": "user",
                "content": user_input,
            })

            response = run_agent(client, messages, tool_schemas)
            print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    main()