
import ollama

from tools import add_task, list_tasks, complete_task, delete_task


MODEL = "qwen2.5:3b"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new business task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The task title",
                    }
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all business tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Complete a task using its numeric ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task using its numeric ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
}


def run_agent(user_message: str) -> str:
    """Let the model choose tools and respond using their results."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a small business operations assistant. "
                "Use tools to manage tasks. Never claim a task was "
                "changed unless a tool confirms it. "
                "Task IDs are numeric. If a user wants to complete "
                "or delete a task but has not identified which one, "
                "ask them for its ID. Do not invent task IDs."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # Allow the model to use tools and then respond to the user.
    for _ in range(5):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        assistant_message = response.message
        tool_calls = assistant_message.tool_calls

        if not tool_calls:
            return assistant_message.content or "I'm not sure how to help."

        messages.append(assistant_message)

        for tool_call in tool_calls:
            name = tool_call.function.name
            arguments = dict(tool_call.function.arguments or {})

            function = AVAILABLE_FUNCTIONS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = function(**arguments)
                except Exception as error:
                    result = f"Tool failed: {error}"

            messages.append(
                {
                    "role": "tool",
                    "name": name,
                    "content": str(result),
                }
            )

    return "I reached the tool-call limit. Please try a simpler request."
