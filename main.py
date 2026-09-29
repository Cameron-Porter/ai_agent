from openai import OpenAI
from pathlib import Path
import tools
import json


client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="local",
)

schema_path = Path(__file__).with_name("tool_schemas.json")
with schema_path.open(encoding="utf-8") as f:
    tool_schemas = json.load(f)

available_tools = {
    "read_file": tools.read_file,
}

messages = [
    {
        "role": "system",
        "content": (
            "You are a local assistant. Use the available tools when "
            "needed to fulfill requests. Base answers about files on "
            "their actual contents, obtained through tools."
        ),
    }
]

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ("exit", "quit"):
        break
    if not user_input.strip():
        continue

    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="qwen",
            messages=messages,
            tools=tool_schemas,
        )

        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            print("Agent:", message.content or "")
            break

        for tool_call in message.tool_calls:
            try:
                arguments = json.loads(tool_call.function.arguments)
                function = available_tools[tool_call.function.name]
                result = function(**arguments)
            except (KeyError, TypeError, ValueError, OSError) as error:
                result = f"Tool error: {error}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })